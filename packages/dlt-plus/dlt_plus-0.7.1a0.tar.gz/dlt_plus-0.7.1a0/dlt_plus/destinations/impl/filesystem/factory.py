from typing import Type, TYPE_CHECKING

from dlt.common.destination import DestinationCapabilitiesContext

from dlt.destinations.impl.filesystem.factory import filesystem as _filesystem

if TYPE_CHECKING:
    from dlt.destinations.impl.filesystem.filesystem import FilesystemClient


class iceberg(_filesystem):
    def _raw_capabilities(self) -> DestinationCapabilitiesContext:
        caps = super()._raw_capabilities()
        caps.preferred_loader_file_format = "parquet"
        caps.supported_loader_file_formats = ["parquet", "reference"]
        caps.preferred_table_format = "iceberg"
        caps.supported_table_formats = ["iceberg"]
        caps.loader_file_format_selector = None
        caps.merge_strategies_selector = None
        caps.supported_merge_strategies = ["delete-insert"]
        return caps

    @property
    def client_class(self) -> Type["FilesystemClient"]:
        from dlt_plus.destinations.impl.filesystem.filesystem import FilesystemClient

        return FilesystemClient


iceberg.register()


class delta(_filesystem):
    def _raw_capabilities(self) -> DestinationCapabilitiesContext:
        caps = super()._raw_capabilities()
        caps.preferred_loader_file_format = "parquet"
        caps.supported_loader_file_formats = ["parquet", "reference"]
        caps.preferred_table_format = "delta"
        caps.supported_table_formats = ["delta"]
        caps.loader_file_format_selector = None
        caps.merge_strategies_selector = None
        caps.supported_merge_strategies = ["upsert"]
        return caps


delta.register()
