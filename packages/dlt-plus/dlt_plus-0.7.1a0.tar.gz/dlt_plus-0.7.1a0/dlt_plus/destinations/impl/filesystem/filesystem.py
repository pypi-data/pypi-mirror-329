from typing import Iterable, List, Any

from dlt.common.destination.client import PreparedTableSchema, LoadJob
from dlt.common.exceptions import MissingDependencyException
from dlt.common.schema.utils import get_columns_names_with_prop, is_nested_table
from dlt.common.schema.exceptions import SchemaCorruptedException
from dlt.common.storages.load_package import ParsedLoadJobFileName

from dlt_plus import version

try:
    from dlt.common.libs.pyiceberg import ensure_iceberg_compatible_arrow_data
    import duckdb
except ImportError:
    raise MissingDependencyException(
        "dlt+ iceberg destination",
        [f"{version.PKG_NAME}[iceberg]"],
        "iceberg needs pyiceberg, pyarrow, sqlalchemy and duckdb in order to work",
    )

from dlt.destinations import duckdb as duckdb_destination
from dlt.destinations.sql_jobs import SqlMergeFollowupJob
from dlt.destinations.impl.filesystem.filesystem import (
    FilesystemClient as _FilesystemClient,
    IcebergLoadFilesystemJob as _IcebergLoadFilesystemJob,
)

from dlt_plus.destinations.utils import get_dedup_sort_order_by_sql


class IcebergLoadFilesystemJob(_IcebergLoadFilesystemJob):
    def run(self) -> None:
        if (
            self._load_table["write_disposition"] == "merge"
            and self._load_table["x-merge-strategy"] == "delete-insert"  # type: ignore[typeddict-item]
        ):
            self._run_delete_insert()
        else:
            super().run()

    def _run_delete_insert(self) -> None:
        from pyiceberg.expressions import In, Or

        def get_delete_filter(primary_keys: List[str], merge_keys: List[str]) -> Any:
            # we know we have one primary key and/or one merge key, because we have already
            # checked this in `verify_schema` method
            assert primary_keys or merge_keys
            assert len(primary_keys) <= 1
            assert len(merge_keys) <= 1
            if primary_keys and merge_keys:
                primary_key, merge_key = primary_keys[0], merge_keys[0]
                key_vals = arrow_table.select([primary_key, merge_key]).to_pydict()
                return Or(
                    In(primary_key, key_vals[primary_key]),
                    In(merge_key, key_vals[merge_key]),
                )
            elif primary_keys:
                primary_key = primary_keys[0]
                key_vals = arrow_table.select([primary_key]).to_pydict()
                return In(primary_key, key_vals[primary_key])
            elif merge_keys:
                merge_key = merge_keys[0]
                key_vals = arrow_table.select([merge_key]).to_pydict()
                return In(merge_key, key_vals[merge_key])

        arrow_table = self.arrow_dataset.to_table()

        # get key from schema and deduplicate if primary key
        if primary_keys := get_columns_names_with_prop(self._load_table, "primary_key"):
            # deduplicate
            order_by = get_dedup_sort_order_by_sql(self._load_table)
            con = duckdb.connect()
            arrow_table = (
                con.sql(f"""
                FROM arrow_table
                QUALIFY row_number() OVER (PARTITION BY {primary_keys[0]} ORDER BY {order_by}) = 1;
            """)
                .arrow()
                .cast(arrow_table.schema)
            )

        # prepare deletes
        merge_keys = get_columns_names_with_prop(self._load_table, "merge_key")
        delete_filter = get_delete_filter(primary_keys, merge_keys)

        # prepare inserts

        # remove hard-deleted records
        caps = duckdb_destination()._raw_capabilities()
        hard_delete_col, not_deleted_cond = SqlMergeFollowupJob._get_hard_delete_col_and_cond(
            self._load_table,
            caps.escape_identifier,
            caps.escape_literal,
            invert=True,
        )
        if hard_delete_col is not None:
            con = duckdb.connect()
            arrow_table = (
                con.execute(f"FROM arrow_table WHERE {not_deleted_cond};")
                .arrow()
                .cast(arrow_table.schema)
            )

        # execute deletes and inserts in single transaction
        with self._iceberg_table().transaction() as txn:
            txn.delete(delete_filter)
            txn.append(ensure_iceberg_compatible_arrow_data(arrow_table))


class FilesystemClient(_FilesystemClient):
    def create_load_job(
        self, table: PreparedTableSchema, file_path: str, load_id: str, restore: bool = False
    ) -> LoadJob:
        # TODO: figure out how to add files:
        # https://binayakd.tech/posts/2024-12-25-register-parquet-files-to-iceberg-without-rewrites/
        job = super().create_load_job(table, file_path, load_id, restore)
        if isinstance(job, _IcebergLoadFilesystemJob):
            job.__class__ = IcebergLoadFilesystemJob
        return job

    def verify_schema(
        self, only_tables: Iterable[str] = None, new_jobs: Iterable[ParsedLoadJobFileName] = None
    ) -> List[PreparedTableSchema]:
        tables = super().verify_schema(only_tables, new_jobs)
        for table in tables:
            if (
                table.get("table_format") == "iceberg"
                and table["write_disposition"] == "merge"
                and table["x-merge-strategy"] == "delete-insert"  # type: ignore[typeddict-item]
            ):
                primary_key = get_columns_names_with_prop(table, "primary_key")
                merge_key = get_columns_names_with_prop(table, "merge_key")
                for key in [primary_key, merge_key]:
                    key_type = "primary_key" if key == primary_key else "merge_key"
                    if len(key) > 1:
                        raise SchemaCorruptedException(
                            self.schema.name,
                            f"Found multiple `{key_type}` columns for table"
                            f""" "{table["name"]}" while only one is allowed when using `iceberg`"""
                            " table format and `delete-insert` merge strategy:"
                            f""" {", ".join([f'"{k}"' for k in key])}.""",
                        )
                if is_nested_table(table):
                    raise SchemaCorruptedException(
                        self.schema.name,
                        f'Found nested table "{table["name"]}". Nested tables are not supported'
                        " when using `iceberg` table format and `delete-insert` merge strategy.",
                    )

        return tables
