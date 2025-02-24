import os
import argparse

from dlt.cli import SupportsCliCommand, echo as fmt, CliCommandException

from dlt_plus.common.cli import add_project_opts

from dlt_plus.project.cli.helpers import project_from_args_with_cli_output
from ..run_context import (
    ProjectRunContext,
    get_profile_pin_file,
    read_profile_pin,
    save_profile_pin,
)
from .helpers import add_profile


class ProfileCommand(SupportsCliCommand):
    command = "profile"
    help_string = "Manage dlt+ project profiles"
    description = """
Commands to manage profiles for project.
Run without arguments to list all profiles, the default profile and the
pinned profile in current project.
"""

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        add_project_opts(parser)

        parser.add_argument("profile_name", help="Name of the profile to add", nargs="?")

        subparsers = parser.add_subparsers(
            title="Available subcommands", dest="profile_command", required=False
        )

        subparsers.add_parser(
            "info",
            help="Show information about profile settings.",
            description="Show information about the current profile.",
        )

        subparsers.add_parser(
            "list",
            help="Show list of all profiles in the project.",
            description="Show list of all profiles in the project.",
        )

        subparsers.add_parser(
            "add",
            help="Add a new profile to the project.",
            description="""
Add a new profile to the project.
""",
        )

        subparsers.add_parser(
            "pin",
            help="Pin a profile to the project.",
            description="""
Pin a profile to the project, this will be the new default profile while it is pinned.
""",
        )

    def execute(self, args: argparse.Namespace) -> None:
        project_run_context = project_from_args_with_cli_output(args)

        if args.profile_command in ["info", "list"]:
            print_profile_info(project_run_context)
        elif args.profile_command == "add":
            add_project_profile(project_run_context, args.profile_name)
        elif args.profile_command == "pin":
            pin_project_profile(project_run_context, args.profile_name)
        else:
            self.parser.print_usage()


def print_profile_info(project_run_context: ProjectRunContext) -> None:
    profiles = list(project_run_context.project.profiles.keys())
    fmt.echo(f"Available profiles: {profiles}")
    fmt.echo(f"Current profile: {project_run_context.profile}")
    fmt.echo(f"Default profile: {project_run_context.project.default_profile}")
    fmt.echo(f"Pinned profile: {read_profile_pin(project_run_context)}")


def add_project_profile(project_run_context: ProjectRunContext, profile_name: str) -> None:
    fmt.echo("Will add a new profile to your dlt+ project.")
    if profile_name in project_run_context.project.profiles:
        fmt.error(f"Profile '{profile_name}' already exists")
        raise CliCommandException()
    if not fmt.confirm("Do you want to proceed?", default=True):
        exit(0)
    add_profile(project_run_context, profile_name)


def pin_project_profile(project_run_context: ProjectRunContext, profile_name: str) -> None:
    if not profile_name:
        pinned_profile = read_profile_pin(project_run_context)
        if pinned_profile:
            pin_file = get_profile_pin_file(project_run_context)
            fmt.echo(
                f"Currently pinned profile is: {pinned_profile}. "
                f"To unpin remove {os.path.relpath(pin_file)} file."
            )
        else:
            fmt.echo("No pinned profile.")
    else:
        fmt.echo(f"Will pin the profile {profile_name} profile to your dlt+ project.")
        if not fmt.confirm("Do you want to proceed?", default=True):
            exit(0)
        save_profile_pin(project_run_context, profile_name)
