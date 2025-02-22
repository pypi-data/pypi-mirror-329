import sys

from pygeai.cli.commands import Command, Option, ArgumentsEnum
from pygeai.cli.commands.builders import build_help_text
from pygeai.cli.commands.options import DETAIL_OPTION, PROJECT_NAME_OPTION, PROJECT_ID_OPTION, SUBSCRIPTION_TYPE_OPTION, \
    USAGE_LIMIT_USAGE_UNIT_OPTION, USAGE_LIMIT_SOFT_LIMIT_OPTION, USAGE_LIMIT_HARD_LIMIT_OPTION, \
    USAGE_LIMIT_RENEWAL_STATUS_OPTION, PROJECT_DESCRIPTION_OPTION
from pygeai.cli.texts.help import ORGANIZATION_HELP_TEXT
from pygeai.core.common.exceptions import MissingRequirementException
from pygeai.organization.clients import OrganizationClient


def show_organization_help():
    """
    Displays help text in stdout
    """
    help_text = build_help_text(organization_commands, ORGANIZATION_HELP_TEXT)
    sys.stdout.write(help_text)


def get_assistant_list(detail: str = "summary"):
    client = OrganizationClient()
    result = client.get_assistant_list(detail)
    sys.stdout.write(f"Assistant list: \n{result}\n")


assistants_list_options = [
    Option(
        "detail",
        ["--detail", "-d"],
        "Defines the level of detail required. The available options are summary (default) or full (optional).",
        True
    ),
]


def get_project_list(option_list: list):
    detail = "summary"
    name = None
    for option_flag, option_arg in option_list:
        if option_flag.name == "detail":
            detail = option_arg
        if option_flag.name == "name":
            name = option_arg

    client = OrganizationClient()
    result = client.get_project_list(detail, name)
    sys.stdout.write(f"Project list: \n{result}\n")


project_list_options = [
    DETAIL_OPTION,
    PROJECT_NAME_OPTION,
]


def get_project_detail(option_list: list):
    project_id = None
    for option_flag, option_arg in option_list:
        if option_flag.name == "project_id":
            project_id = option_arg

    if not project_id:
        raise MissingRequirementException("Cannot retrieve project detail without project-id")

    client = OrganizationClient()
    result = client.get_project_data(project_id=project_id)
    sys.stdout.write(f"Project detail: \n{result}\n")


project_detail_options = [
    PROJECT_ID_OPTION,
]


def create_project(option_list: list):
    name = None
    email = None
    description = None
    subscription_type = None
    usage_unit = None
    soft_limit = None
    hard_limit = None
    renewal_status = None
    usage_limit = {}

    for option_flag, option_arg in option_list:
        if option_flag.name == "name":
            name = option_arg

        if option_flag.name == "description":
            description = option_arg

        if option_flag.name == "admin_email":
            email = option_arg

        if option_flag.name == "subscription_type":
            subscription_type = option_arg

        if option_flag.name == "usage_unit":
            usage_unit = option_arg

        if option_flag.name == "soft_limit":
            soft_limit = option_arg

        if option_flag.name == "hard_limit":
            hard_limit = option_arg

        if option_flag.name == "renewal_status":
            renewal_status = option_arg

    if subscription_type or usage_unit or soft_limit or hard_limit or renewal_status:
        usage_limit.update({
            "subscriptionType": subscription_type,
            "usageUnit": usage_unit,
            "softLimit": soft_limit,
            "hardLimit": hard_limit,
            "renewalStatus": renewal_status
        })

    if not (name and email):
        raise MissingRequirementException("Cannot create project without name and administrator's email")

    client = OrganizationClient()
    result = client.create_project(name, email, description)
    sys.stdout.write(f"New project: \n{result}\n")


create_project_options = [
    Option(
        "name",
        ["--name", "-n"],
        "Name of the new project",
        True
    ),
    Option(
        "description",
        ["--description", "-d"],
        "Description of the new project",
        True
    ),
    Option(
        "admin_email",
        ["--email", "-e"],
        "Project administrator's email",
        True
    ),
    SUBSCRIPTION_TYPE_OPTION,
    USAGE_LIMIT_USAGE_UNIT_OPTION,
    USAGE_LIMIT_SOFT_LIMIT_OPTION,
    USAGE_LIMIT_HARD_LIMIT_OPTION,
    USAGE_LIMIT_RENEWAL_STATUS_OPTION
]


def update_project(option_list: list):
    project_id = None
    name = None
    description = None
    for option_flag, option_arg in option_list:
        if option_flag.name == "project_id":
            project_id = option_arg

        if option_flag.name == "name":
            name = option_arg

        if option_flag.name == "description":
            description = option_arg

    if not (project_id and name):
        raise MissingRequirementException("Cannot update project without project-id and/or name")

    client = OrganizationClient()
    result = client.update_project(project_id, name, description)
    sys.stdout.write(f"Updated project: \n{result}\n")


update_project_options = [
    PROJECT_ID_OPTION,
    PROJECT_NAME_OPTION,
    PROJECT_DESCRIPTION_OPTION,
]


def delete_project(option_list: list):
    project_id = None
    for option_flag, option_arg in option_list:
        if option_flag.name == "project_id":
            project_id = option_arg

    if not project_id:
        raise MissingRequirementException("Cannot delete project without project-id")

    client = OrganizationClient()
    result = client.delete_project(project_id)
    sys.stdout.write(f"Deleted project: \n{result}\n")


delete_project_options = [
    PROJECT_ID_OPTION,
]


def get_project_tokens(option_list: list):
    project_id = None
    for option_flag, option_arg in option_list:
        if option_flag.name == "project_id":
            project_id = option_arg

    if not project_id:
        raise MissingRequirementException("Cannot retrieve project tokens without project-id")

    client = OrganizationClient()
    result = client.get_project_tokens(project_id)
    sys.stdout.write(f"Project tokens: \n{result}\n")


get_project_tokens_options = [
    PROJECT_ID_OPTION,
]


def export_request_data(option_list: list):
    assistant_name = None
    status = None
    skip = 0
    count = 0
    for option_flag, option_arg in option_list:
        if option_flag.name == "assistant_name":
            assistant_name = option_arg

        if option_flag.name == "status":
            status = option_arg

        if option_flag.name == "skip":
            skip = option_arg

        if option_flag.name == "count":
            count = option_arg

    client = OrganizationClient()
    result = client.export_request_data(assistant_name, status, skip, count)
    sys.stdout.write(f"Request data: \n{result}\n")


export_request_data_options = [
    Option(
        "assistant_name",
        ["--assistant-name"],
        "string: Assistant name (optional)",
        True
    ),
    Option(
        "status",
        ["--status"],
        "string: Status (optional)",
        True
    ),
    Option(
        "skip",
        ["--skip"],
        "integer: Number of entries to skip",
        True
    ),
    Option(
        "count",
        ["--count"],
        "integer: Number of entries to retrieve",
        True
    )
]

organization_commands = [
    Command(
        "help",
        ["help", "h"],
        "Display help text",
        show_organization_help,
        ArgumentsEnum.NOT_AVAILABLE,
        [],
        []
    ),
    Command(
        "assistants_list",
        ["list-assistants"],
        "List assistant information",
        get_assistant_list,
        ArgumentsEnum.OPTIONAL,
        [],
        assistants_list_options
    ),
    Command(
        "project_list",
        ["list-projects"],
        "List project information",
        get_project_list,
        ArgumentsEnum.OPTIONAL,
        [],
        project_list_options
    ),
    Command(
        "project_detail",
        ["get-project"],
        "Get project information",
        get_project_detail,
        ArgumentsEnum.REQUIRED,
        [],
        project_detail_options
    ),
    Command(
        "create_project",
        ["create-project"],
        "Create new project",
        create_project,
        ArgumentsEnum.REQUIRED,
        [],
        create_project_options
    ),
    Command(
        "update_project",
        ["update-project"],
        "Update existing project",
        update_project,
        ArgumentsEnum.REQUIRED,
        [],
        update_project_options
    ),
    Command(
        "delete_project",
        ["delete-project"],
        "Delete existing project",
        delete_project,
        ArgumentsEnum.REQUIRED,
        [],
        delete_project_options
    ),
    Command(
        "get_project_tokens",
        ["get-tokens"],
        "Get project tokens",
        get_project_tokens,
        ArgumentsEnum.REQUIRED,
        [],
        get_project_tokens_options
    ),
    Command(
        "export_request_data",
        ["export-request"],
        "Export request data",
        export_request_data,
        ArgumentsEnum.OPTIONAL,
        [],
        export_request_data_options
    ),
]
