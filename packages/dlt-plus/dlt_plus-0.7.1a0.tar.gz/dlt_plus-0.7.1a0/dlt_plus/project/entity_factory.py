from typing import Any, Optional, Union, TYPE_CHECKING, Dict, List

import dlt
from dlt.common import logger
from dlt.common.destination import AnyDestination, Destination
from dlt.common.schema import Schema
from dlt.common.typing import Unpack
from dlt.sources import AnySourceFactory, SourceReference

from dlt_plus.destinations.dataset import WritableDataset


if TYPE_CHECKING:
    from dlt_plus.transformations.transformations import Transformation
    from dlt_plus.transformations.config import TransformationConfig
    from dlt_plus.cache.cache import Cache
else:
    Transformation = Any
    TransformationConfig = Any
    Cache = Any

from .config.config import Project
from .config.typing import DatasetConfig, PipelineConfig, SourceConfig, DestinationConfig
from .exceptions import ProjectException, ProjectExplicitEntityNotFound, InvalidDestinationException


class EntityFactory:
    def __init__(self, project_config: Project):
        self.project_config = project_config

    def create_source_factory(self, source_ref_or_name: str) -> AnySourceFactory:
        """Creates source factory from explicit name or a reference"""
        source_config = self._get_source_config(source_ref_or_name)
        if source_config is None:
            # no specific config, assumes we use source ref
            source_config = {}

        # get source type from config or use source name as reference
        # this makes source implicit
        source_type = source_config.get("type") or source_ref_or_name

        # check if "with_args" is present
        with_args_dict = source_config.get("with_args") or {}
        # Override the default section name with the source name to make the configuration
        # compatible with the CustomLoaderDocProvider we are using in config.Config
        source_factory = SourceReference.find(source_type).clone(
            name=source_ref_or_name, section=source_ref_or_name, **with_args_dict
        )
        return source_factory

    def create_destination(self, destination_ref_or_name: str) -> AnyDestination:
        destination_config = self._get_destination_config(destination_ref_or_name)
        if destination_config is None:
            # allows for ad hoc destinations
            destination_config = {}

        # accept destination factory instance
        if isinstance(destination_config, Destination):
            return destination_config

        if destination_type := destination_config.get("type"):
            # create named destination
            return Destination.from_reference(
                destination_type, destination_name=destination_ref_or_name
            )
        else:
            # if destination does not have a type, use shorthand notation
            return Destination.from_reference(destination_ref_or_name)

    def create_dataset(
        self,
        dataset_name: str,
        destination_name: str = None,
        schema: Union[Schema, str, None] = None,
    ) -> WritableDataset:
        # force if datasets must be explicit
        dataset_config = self._get_dataset_config(dataset_name)
        # get possible destinations for dataset_name using explicit config and available pipelines
        available_destinations = self._resolve_dataset_destinations(dataset_name)
        if not destination_name:
            destination_name = available_destinations[0]
        elif destination_name not in available_destinations:
            # TODO: define exception
            raise InvalidDestinationException(
                self.project_config.project_dir,
                dataset_name,
                destination_name,
                available_destinations,
            )
        return WritableDataset(
            dataset_config,
            destination=self.create_destination(available_destinations[0]),
            dataset_name=dataset_name,
            schema=schema,
        )

    def create_cache(self, name: str) -> Cache:
        from dlt_plus.cache.cache import create_cache as _create_cache

        available_caches = list(self.project_config.caches.keys())

        # TODO: allow for explicit cache with default settings, we can also implement cache registry
        if not available_caches:
            raise ProjectException(self.project_config.project_dir, "No caches found in project.")

        # TODO: apply the . notation to all entities or drop it
        if not name or name == ".":
            name = available_caches[0]
            logger.info(f"No cache name given, taking the first discovered: {name}")

        cache_config = self.project_config.caches.get(name)

        if not cache_config:
            raise ProjectExplicitEntityNotFound(self.project_config.project_dir, "cache", name)

        # create dataset instances from strings
        cache_config["name"] = name
        # create factories from config
        for input in cache_config.get("inputs", []):
            dataset = input["dataset"]
            if isinstance(dataset, str):
                input["dataset"] = self.create_dataset(dataset)
        for output in cache_config.get("outputs", []):
            dataset = output["dataset"]
            if isinstance(dataset, str):
                output["dataset"] = self.create_dataset(dataset)

        return _create_cache(cache_config)

    def create_transformation(self, name: str) -> Transformation:
        """Get transformation by name"""
        from dlt_plus.transformations.transformations import (
            create_transformation as _create_transformation,
        )

        # TODO: apply the . notation to all entities or drop it
        available_ts = list(self.project_config.transformations.keys())

        if not available_ts:
            raise ProjectException(
                self.project_config.project_dir, "No transformations found in project."
            )

        if not name or name == ".":
            name = available_ts[0]
            logger.info(f"No transformation name given, taking the first discovered: {name}")

        transformation_config: TransformationConfig
        if transformation_config := self.project_config.transformations.get(name):
            transformation_config["name"] = name
            # resolve cache
            if cache_name := transformation_config.get("cache"):
                transformation_config["cache"] = self.create_cache(cache_name)
            return _create_transformation(transformation_config)
        else:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "transformation", name
            )

    def create_pipeline(
        self, pipeline_name: str, **explicit_config: Unpack[PipelineConfig]
    ) -> dlt.Pipeline:
        """Creates a pipeline using expicitly declared `pipeline_name` or by pipeline
        registry (tbd.)

        Applies `explict_config` that may be passed by pipeline runner to override defaults.
        """

        pipeline_config = self._get_pipeline_config(pipeline_name)
        if pipeline_config is None:
            pipeline_config = {}
        if explicit_config:
            # apply explicit config, make sure we create copy not to change the original
            pipeline_config = {**pipeline_config, **explicit_config}

        destination_name = pipeline_config.get("destination")
        if not destination_name:
            raise ProjectException(
                self.project_config.project_dir,
                f"Destination is not defined for pipeline '{pipeline_name}'",
            )

        # verify if a valid dataset exists
        dataset_name = pipeline_config.get("dataset_name")
        if not dataset_name:
            raise ProjectException(
                self.project_config.project_dir,
                f"Dataset is not defined for pipeline '{pipeline_name}'",
            )

        # create dataset, which also creates destination and does required checks
        # NOTE: destination is not physically accessed
        dataset_ = self.create_dataset(dataset_name, destination_name)
        return dlt.pipeline(
            pipeline_name,
            destination=dataset_._destination,
            dataset_name=dataset_name,
        )

    @property
    def allow_undefined_entities(self) -> bool:
        return self.project_config.settings.get("allow_undefined_entities", True)

    def _get_pipeline_config(self, pipeline_name: str) -> Optional[PipelineConfig]:
        pipeline_config = self.project_config.pipelines.get(pipeline_name)
        if not self.allow_undefined_entities and not pipeline_config:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "pipeline", pipeline_name
            )
        # TODO: consider cloning all configs to prevent modification of the original
        return pipeline_config

    def _get_source_config(self, source_name: str) -> Optional[SourceConfig]:
        source_config = self.project_config.sources.get(source_name)
        if not self.allow_undefined_entities and not source_config:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "source", source_name
            )
        return source_config

    def _get_destination_config(self, destination_name: str) -> Optional[DestinationConfig]:
        destination_config = self.project_config.destinations.get(destination_name)
        if not self.allow_undefined_entities and not destination_config:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "destination", destination_name
            )
        return destination_config

    def _get_dataset_config(self, dataset_name: str) -> Optional[DatasetConfig]:
        dataset_config = self.project_config.datasets.get(dataset_name)
        if not self.allow_undefined_entities and not dataset_config:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "dataset", dataset_name
            )
        return dataset_config

    def _resolve_dataset_destinations(self, dataset_name: str) -> List[str]:
        """Infers possible destinations from the pipelines if not explicitly limited"""

        dataset_config = self._get_dataset_config(dataset_name) or {}
        available_destinations = dataset_config.get("destination")

        # if no explicit destinations, take them from defined pipelines
        if available_destinations is None:
            available_destinations = []
            for pipeline_config in self.project_config.pipelines.values():
                if pipeline_config:
                    if dataset_name == pipeline_config.get("dataset_name"):
                        if destination_name := pipeline_config.get("destination"):
                            available_destinations.append(destination_name)

        if not available_destinations:
            raise InvalidDestinationException(
                self.project_config.project_dir,
                dataset_name,
                None,
                available_destinations,
            )

        # deduplicate but preserve order
        seen: Dict[str, str] = {}
        return [seen.setdefault(x, x) for x in available_destinations if x not in seen]
