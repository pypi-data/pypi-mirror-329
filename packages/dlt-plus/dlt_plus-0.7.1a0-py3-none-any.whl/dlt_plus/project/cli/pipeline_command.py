from typing import List

import argparse

import dlt
from dlt.cli import echo as fmt
from dlt.cli.plugins import PipelineCommand
from dlt.common import logger

from dlt_plus.common.cli import add_project_opts, get_existing_subparser

from dlt_plus.project.cli.helpers import project_from_args_with_cli_output
from ..pipeline_manager import PipelineManager

from .helpers import add_pipeline
from ..run_context import (
    ProjectRunContext,
)

from .formatters import print_entity_list


class ProjectPipelineCommand(PipelineCommand):
    description = """
The `dlt pipeline` command provides a set of commands to inspect the pipeline working directory,
tables, and data in the destination and check for problems encountered during data loading.

Run without arguments to list all pipelines in the current project.
    """

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        # add opts to switch project / profile
        add_project_opts(parser)
        super().configure_parser(parser)

        subparsers = get_existing_subparser(parser)

        # NOTE: the pipeline parser interface should be changed to
        # dlt pipeline run <pipeline_name> in the core lib

        subparsers.add_parser(
            "list",
            help="List all pipelines in the project.",
            description="List all pipelines in the project.",
        )

        add_parser = subparsers.add_parser(
            "add",
            help="Add a new pipeline to the current project",
            description="""
Adds a new pipeline to the current project. Will not create any sources
or destinations, you can reference other entities by name.
""",
        )

        add_parser.add_argument("source_name", help="Name of the source to add")
        add_parser.add_argument("destination_name", help="Name of the destination to add")
        add_parser.add_argument("--dataset-name", help="Name of the dataset to add", default=None)

        run_parser = subparsers.add_parser("run", help="Run a pipeline")
        run_parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Limits the number of extracted pages for all resources. See source.add_limit.",
        )
        run_parser.add_argument(
            "--resources",
            type=lambda s: [item.strip() for item in s.split(",")],
            help="Comma-separated list of resource names.",
        )

        subparsers.add_parser("mcp", help="Run the MCP server for a pipeline")

    def execute(self, args: argparse.Namespace) -> None:
        if args.operation in ("add", "run"):
            run_context = project_from_args_with_cli_output(args)
            # must have project context
            if args.operation == "add":
                add_project_pipeline(
                    run_context,
                    args.pipeline_name,
                    args.source_name,
                    args.destination_name,
                    args.dataset_name,
                )
            elif args.operation == "run":
                run_pipeline(run_context, args.pipeline_name, args.limit, args.resources)
        # optional project context
        elif args.list_pipelines or args.operation in ("list", "mcp"):
            run_context = project_from_args_with_cli_output(args, allow_no_project=True)
            if args.operation == "list" or args.list_pipelines:
                # NOTE: by default list pipelines in project if no operation is specified
                # we could change this in the core
                if run_context:
                    list_pipelines(run_context)
                else:
                    try:
                        super().execute(args)
                    except Exception:
                        fmt.echo(
                            "No pipeline dirs found in %s" % dlt.current.run_context().data_dir
                        )
            elif args.operation == "mcp":
                from mcp.server.fastmcp import FastMCP
                from dlt_plus.project.mcp_tools import PipelineMCPTools

                logger.info("Starting MCP server for pipeline %s", args.pipeline_name)
                pipeline = dlt.attach(args.pipeline_name)
                pipeline_tools = PipelineMCPTools(pipeline)

                mcp = FastMCP(f"dlt+ pipeline: {args.pipeline_name}")
                pipeline_tools.register_with(mcp)

                mcp.run(transport="stdio")
        # no project context required
        else:
            # execute regular pipeline command without project context
            super().execute(args)


def list_pipelines(run_context: ProjectRunContext) -> None:
    print_entity_list(
        "pipeline",
        [
            f"{name}: {config.get('source')} to {config.get('destination')}"
            for name, config in run_context.project.pipelines.items()
        ],
    )


def add_project_pipeline(
    run_context: ProjectRunContext,
    pipeline_name: str,
    source_name: str,
    destination_name: str,
    dataset_name: str = None,
) -> None:
    # TODO: we could autocreate source and destination if not present and a certain flag
    # is set, not sure..
    fmt.echo("Will add a new pipeline to your dlt+ project.")
    if source_name not in run_context.project.sources.keys():
        fmt.warning(
            "Source %s does not exist in project, your pipeline will "
            "reference a non-existing source." % source_name
        )
    if destination_name not in run_context.project.destinations.keys():
        fmt.warning(
            "Destination %s does not exist in project, your pipeline will "
            "reference a non-existing destination." % destination_name
        )
    if not fmt.confirm("Do you want to proceed?", default=True):
        exit(0)
    add_pipeline(run_context, pipeline_name, source_name, destination_name, dataset_name)


def run_pipeline(
    run_context: ProjectRunContext, pipeline_name: str, limit: int, resources: List[str]
) -> None:
    # TODO: display pre-run info: does the pipeline exist? does it have pending data
    # (we skip extract otherwise)
    # are we changing destination or dataset? do we drop any data if so ask for permission.
    # TODO: now we support explicit config so ad hoc pipelines can be run
    #   we just need to take source_ref, destination ref and dataset name and pass it

    pipeline_manager = PipelineManager(run_context.project)
    load_info = pipeline_manager.run_pipeline(pipeline_name, limit=limit, resources=resources)
    fmt.echo(load_info)
