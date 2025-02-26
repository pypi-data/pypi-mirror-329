from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null


class WorkspaceParser:
    def workspace_parser(subparser):
        create_workspace = subparser.add_parser(
            'create',
            help='Create a new workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_workspace.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to create workspace."
        )
        create_workspace.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create workspace."
        )
        create_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_workspace = subparser.add_parser(
            'list',
            help='List all available workspaces.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_workspace.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable as true or false to list Workspaces."
        )
        list_workspace.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Workspaces for a specific page_number."
        )
        list_workspace.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Workspaces."
        )
        list_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_workspace = subparser.add_parser(
            'search',
            help='Search for workspaces by name.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_workspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace name to search workspaces."
        )
        search_workspace.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable as true or false to search workspaces."
        )
        search_workspace.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search workspaces for a specific page_number."
        )
        search_workspace.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of workspaces."
        )
        search_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_wokspace = subparser.add_parser(
            'get',
            help='Get details of a specific workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_wokspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_id to get information about a specific Workspace."
        )
        get_wokspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_name to get information about a specific Workspace."
        )
        get_wokspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_wokspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_stats_wokspace = subparser.add_parser(
            'get-stats',
            help='Get Spark job statistics for a specific workspace by its ID or Name.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_stats_wokspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the ID of the workspace to retrieve stats."
        )
        get_stats_wokspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the name of the workspace to retrieve stats."
        )
        get_stats_wokspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_stats_wokspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_workspace = subparser.add_parser(
            'edit',
            help='Modify details of a specific workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_workspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_id to edit a specific Workspace."
        )
        edit_workspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_name to edit a specific Workspace."
        )
        edit_workspace.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to edit a specific Workspace."
        )
        edit_workspace.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to edit a specific Workspace."
        )
        edit_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        enable_workspace = subparser.add_parser(
            'enable',
            help='Enable a specific workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        enable_workspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_id to enable a specific Workspace."
        )
        enable_workspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_name to enable a specific Workspace."
        )
        enable_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        enable_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        disable_workspace = subparser.add_parser(
            'disable',
            help='Disable a specific workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        disable_workspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_id to disable a specific Workspace."
        )
        disable_workspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace_name to disable a specific Workspace."
        )
        disable_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        disable_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        export_workspace = subparser.add_parser(
            'export',
            help='Export a specific workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        export_workspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace id to export a specific workspace."
        )
        export_workspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace name to export a specific workspace."
        )
        export_workspace.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable to export active job and notebook configurations of a specific workspace."
        )
        export_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        export_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        import_workspace = subparser.add_parser(
            'import',
            help='Import a specific workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        import_workspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace id to import a specific workspace to it."
        )
        import_workspace.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide workspace name to import a specific workspace."
        )
        import_workspace.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance id to attach with job configurations in the workspace to be imported."
        )
        import_workspace.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance name to attach with job configurations in the workspace to be imported."
        )
        import_workspace.add_argument(
            "--permissive",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide permissive option for partial imports when encountering errors."
        )
        import_workspace.add_argument(
            "--overwrite",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide overwrite option to override any existsing workspace."
        )
        import_workspace.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide file path from where a specific workspace is to be imported."
        )
        import_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        import_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
