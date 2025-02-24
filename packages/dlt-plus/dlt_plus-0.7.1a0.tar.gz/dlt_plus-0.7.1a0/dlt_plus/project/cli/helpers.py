from importlib import resources
from typing import Dict, Any, List, Tuple
import os
import tomlkit
import importlib

import argparse

from ruamel.yaml import YAML

from dlt.cli import echo as fmt, CliCommandException
from dlt.common.destination.reference import DestinationReference
from dlt.common.configuration.providers import (
    SecretsTomlProvider,
)
from dlt.cli.config_toml_writer import WritableConfigValue, write_values
from dlt.extract.reference import SourceReference

from dlt_plus.project.run_context import (
    ProjectRunContext,
    project_from_args,
    ProjectRunContextNotAvailable,
    switch_context,
)
from dlt_plus.common.constants import DEFAULT_PROJECT_CONFIG_FILE
from dlt_plus.project._templates.project import GIT_IGNORE

BASE_TEMPLATES_PATH = "dlt_plus.project._templates"
SOURCES_TEMPLATES_PATH = BASE_TEMPLATES_PATH + ".sources"
DESTINATIONS_TEMPLATES_PATH = BASE_TEMPLATES_PATH + ".destinations"
PROJECT_TEMPLATES_PATH = BASE_TEMPLATES_PATH + ".project"
REQUIREMENTS_FILE_NAME = "requirements.txt"
PYPROJECT_FILE_NAME = "pyproject.toml"
PACKAGE_INIT_FILE_NAME = "package_init.py"


def project_from_args_with_cli_output(
    args: argparse.Namespace, allow_no_project: bool = False
) -> ProjectRunContext:
    try:
        return project_from_args(args)
        # fmt.note(
        #     "Project Context: %s @ %s. Active profile: %s."
        #     % (run_context.name, run_context.run_dir, run_context.profile)
        # )
    except ProjectRunContextNotAvailable:
        if not allow_no_project:
            fmt.error(
                "No project context found. This cli command requires a project context, "
                "get started with `dlt project init` to create a new project."
            )
            raise
    return None


def _read_project_yaml(project_run_context: ProjectRunContext) -> Any:
    """Read the project yaml file."""

    yaml = YAML()
    project_yaml_path = os.path.join(project_run_context.run_dir, DEFAULT_PROJECT_CONFIG_FILE)
    with open(project_yaml_path, "r", encoding="utf-8") as file:
        return yaml.load(file)


def _write_project_yaml(project_dir: str, project_yaml: Any) -> None:
    """Write the project yaml file."""

    yaml = YAML()
    project_yaml_path = os.path.join(project_dir, DEFAULT_PROJECT_CONFIG_FILE)
    with open(project_yaml_path, "w", encoding="utf-8") as file:
        yaml.dump(project_yaml, file)


def _ensure_unique_name(given_name: str, existing_keys: List[str]) -> None:
    """Create a unique name by appending a number to the given name if it already exists."""
    if given_name in existing_keys:
        fmt.error(f"Name {given_name} already exists in project. Please use a different name.")
        raise CliCommandException()


def ensure_project_dirs(project_run_context: ProjectRunContext) -> None:
    """Ensure the project directories exist."""
    os.makedirs(project_run_context.settings_dir, exist_ok=True)


# TODO: all the commands below write files, do some checks then write more files etc.
# they should rather prepare files to copy, keep files to save in memory and then save at the end
# also confirmations should provide some context ie. what will be modified and what got created
# OSS does that so you can check


def init_project(root_dir: str, name: str = None, package_name: str = None) -> ProjectRunContext:
    """
    Initialize a new dlt+ project in the given
    directory by copying the default project template
    If package_name is provided, the project will be initialized as a pip package
    """

    yaml = YAML()

    with resources.open_text(PROJECT_TEMPLATES_PATH, DEFAULT_PROJECT_CONFIG_FILE) as file:
        project_yaml = yaml.load(file)

    if name:
        project_yaml["project"] = project_yaml.get("project") or {}
        project_yaml["project"]["name"] = name

    # get package dir if package, fallback to root dir if not available
    package_dir = os.path.join(root_dir, package_name) if package_name else root_dir
    os.makedirs(package_dir, exist_ok=True)

    # write projec yaml
    _write_project_yaml(package_dir, project_yaml)

    # get install deps
    from dlt_plus.version import __version__ as dlt_plus_version
    from dlt.version import __version__ as dlt_version

    dependencies = [f"dlt=={dlt_version}", f"dlt-plus=={dlt_plus_version}"]

    # write pyproject.toml and package init file if package
    if package_name:
        pptoml = tomlkit.load(resources.open_text(PROJECT_TEMPLATES_PATH, PYPROJECT_FILE_NAME))
        pptoml["project"]["name"] = package_name  # type: ignore
        pptoml["project"]["dependencies"] = dependencies  # type: ignore
        pptoml["project"]["entry-points"]["dlt_package"]["dlt-project"] = package_name  # type: ignore
        with open(os.path.join(root_dir, "pyproject.toml"), "w", encoding="utf-8") as f:
            tomlkit.dump(pptoml, f)

        with resources.open_text(PROJECT_TEMPLATES_PATH, PACKAGE_INIT_FILE_NAME) as file:
            with open(os.path.join(package_dir, "__init__.py"), "w", encoding="utf-8") as f:
                f.write(file.read())

    # write requirements if not package
    else:
        with open(os.path.join(root_dir, REQUIREMENTS_FILE_NAME), "w", encoding="utf-8") as f:
            f.write("\n".join(dependencies))

    # retrieve context
    project_run_context = switch_context(package_dir)

    # create sources dir
    ensure_project_dirs(project_run_context)

    # copy default toml files
    for fname in ["secrets.toml", "config.toml"]:
        with open(
            os.path.join(project_run_context.settings_dir, fname), "w", encoding="utf-8"
        ) as f:
            f.write(f"# default {fname} file")

    # create gitignore file
    with open(os.path.join(root_dir, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(GIT_IGNORE)

    return project_run_context


def add_profile(project_run_context: ProjectRunContext, profile_name: str) -> None:
    """Add a profile to the project."""
    project_yaml = _read_project_yaml(project_run_context)
    project_yaml["profiles"] = project_yaml.get("profiles") or {}
    project_yaml["profiles"][profile_name] = {}
    _write_project_yaml(project_run_context.run_dir, project_yaml)

    # create profile secrets file
    with open(
        os.path.join(project_run_context.settings_dir, f"{profile_name}.secrets.toml"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"# secrets for profile {profile_name}\n")


def add_source(
    project_run_context: ProjectRunContext,
    source_name: str,
    source_type: str = None,
) -> str:
    """Add a source to the project, returns the name."""
    ensure_project_dirs(project_run_context)

    project_yaml = _read_project_yaml(project_run_context)
    project_yaml["sources"] = project_yaml.get("sources") or {}

    # ensure unique name
    source_type = source_type or source_name
    _ensure_unique_name(source_name, project_yaml["sources"].keys())

    # check if source is a template in the sources folder
    # if so, copy file to sources dir
    if resources.is_resource(SOURCES_TEMPLATES_PATH, f"{source_type}.py"):
        sources_dir = os.path.join(project_run_context.run_dir, "sources")
        os.makedirs(sources_dir, exist_ok=True)
        with resources.open_text(SOURCES_TEMPLATES_PATH, f"{source_type}.py") as file:
            with open(os.path.join(sources_dir, f"{source_name}.py"), "w", encoding="utf-8") as f:
                f.write(file.read())

        # point to copied template
        source_type = f"sources.{source_name}.source"

    # look up source and update configs
    source_spec = SourceReference.find(
        source_type,
        raise_exec_errors=True,
        import_missing_modules=True,
    ).ref.SPEC

    # TODO: the following code injects examples for sql_database and rest_api, which we should
    # make available as configspec features in the core so it will work via write_values
    template = None
    if source_type == "rest_api":
        template = """
[sources.{source_name}]
resources = ["pokemon", "berry"] # please set me up!
[sources.{source_name}.client] # please set me up!
base_url= "https://pokeapi.co/api/v2/"
"""
    elif source_type == "sql_database":
        template = """
[sources.{source_name}]
table_names = ["family", "clan"]
[sources.{source_name}.credentials]
drivername = "mysql+pymysql"
database = "Rfam"
username = "rfamro"
host = "mysql-rfam-public.ebi.ac.uk"
port = 4497
"""

    if template:
        with open(
            os.path.join(project_run_context.settings_dir, "secrets.toml"),
            "a",
            encoding="utf-8",
        ) as f:
            f.write(template.replace("{source_name}", source_name))
    else:
        source_secrets = WritableConfigValue(source_name, source_spec, None, ("sources",))
        secrets_provider = SecretsTomlProvider(settings_dir=project_run_context.settings_dir)
        write_values(secrets_provider._config_toml, [source_secrets], overwrite_existing=False)
        secrets_provider.write_toml()

    # update project yaml
    project_yaml["sources"][source_name] = {
        "type": source_type,
    }
    _write_project_yaml(project_run_context.run_dir, project_yaml)

    return source_name


def add_dataset(
    project_run_context: ProjectRunContext, dataset_name: str, destination_name: str
) -> str:
    """Add a dataset to the project, returns the name."""
    project_yaml = _read_project_yaml(project_run_context)
    project_yaml["datasets"] = project_yaml.get("datasets") or {}

    # create name
    _ensure_unique_name(dataset_name, project_yaml["datasets"].keys())

    # add dataset to yaml
    project_yaml["datasets"][dataset_name] = {
        "destination": [destination_name],
    }

    _write_project_yaml(project_run_context.run_dir, project_yaml)

    return dataset_name


def add_destination(
    project_run_context: ProjectRunContext,
    destination_name: str,
    destination_type: str = None,
    dataset_name: str = None,
) -> Tuple[str, str]:
    """Add a destination to the project, returns the name."""
    ensure_project_dirs(project_run_context)

    # look up destination
    destination_type = destination_type or destination_name
    destination_ref = DestinationReference.find(
        destination_type,
        raise_exec_errors=True,
        import_missing_modules=True,
    )
    # extract factory if we resolve custom destination (decorator)
    destination_ref = DestinationReference.ensure_factory(destination_ref)

    # create unique name
    project_yaml = _read_project_yaml(project_run_context)
    project_yaml["destinations"] = project_yaml.get("destinations") or {}
    _ensure_unique_name(destination_name, project_yaml["destinations"].keys())

    project_yaml["destinations"][destination_name] = {
        "type": destination_type,
    }
    _write_project_yaml(project_run_context.run_dir, project_yaml)

    # extract secrets to toml file
    destination_secrets = WritableConfigValue(
        destination_name, destination_ref.spec, None, ("destination",)
    )
    secrets_provider = SecretsTomlProvider(settings_dir=project_run_context.settings_dir)
    write_values(secrets_provider._config_toml, [destination_secrets], overwrite_existing=False)
    secrets_provider.write_toml()

    # add a dataset for this destination
    if dataset_name:
        dataset_name = dataset_name or destination_name + "_dataset"
        dataset_name = add_dataset(project_run_context, dataset_name, destination_name)
    else:
        dataset_name = None

    return destination_name, dataset_name


def add_pipeline(
    project_run_context: ProjectRunContext,
    pipeline_name: str,
    source_name: str,
    destination_name: str,
    dataset_name: str = None,
) -> None:
    """Add a pipeline to the project, returns the name."""
    project_yaml = _read_project_yaml(project_run_context)
    project_yaml["pipelines"] = project_yaml.get("pipelines") or {}

    # create name
    _ensure_unique_name(pipeline_name, project_yaml["pipelines"].keys())

    # add pipeline to yaml
    project_yaml["pipelines"][pipeline_name] = {
        "source": source_name,
        "destination": destination_name,
    }

    # add dataset name if provided
    if dataset_name:
        project_yaml["pipelines"][pipeline_name]["dataset_name"] = dataset_name
    else:
        project_yaml["pipelines"][pipeline_name]["dataset_name"] = pipeline_name + "_dataset"

    _write_project_yaml(project_run_context.run_dir, project_yaml)


def get_available_destinations() -> List[str]:
    """Get all available destinations."""
    return [
        d.replace("dlt_plus.destinations.", "").replace("dlt.destinations.", "")
        for d in DestinationReference.DESTINATIONS.keys()
    ]


def get_available_source() -> Dict[str, str]:
    """Get all available destinations."""
    # TODO: for some reason not all sources are in SourceReference.SOURCES
    # so for now we fake it here
    # TODO: reuse OSS logic that lists verified sources (it imports module from known location)
    #  and then find SOURCES in that location. we will not import sources automatically
    #  because that slows down the startup
    return {
        "sql_database": "SQL Database Source",
        "rest_api": "REST API Source",
        "filesystem": "Source for files and folders, csv, json, parquet, etc.",
    }


def get_available_source_templates() -> Dict[str, str]:
    """Get all available source templates."""
    # if resources.is_resource(SOURCES_TEMPLATES_PATH, f"{source_type}.py"):

    templates: Dict[str, str] = {}
    for source_template in resources.contents(package=SOURCES_TEMPLATES_PATH):
        if source_template.startswith("_"):
            continue
        module_name = source_template.replace(".py", "")
        source = importlib.import_module(SOURCES_TEMPLATES_PATH + "." + module_name)
        templates[module_name] = source.__doc__

    return templates
