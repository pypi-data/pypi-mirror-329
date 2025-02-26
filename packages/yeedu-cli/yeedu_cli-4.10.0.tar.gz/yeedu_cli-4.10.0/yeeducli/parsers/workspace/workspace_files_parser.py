from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class WorkspaceFilesParser:

    def workspace_files_parser(subparser):
        create_workspace_files = subparser.add_parser(
            'create-workspace-file',
            help='To create a Workspace Files.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_workspace_files.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Id to create-workspace-file."
        )
        create_workspace_files.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Name to to create-workspace-file."
        )
        create_workspace_files.add_argument(
            "--local_file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide local_file_path to create-workspace-file."
        )
        create_workspace_files.add_argument(
            "--overwrite",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide overwrite to create-workspace-file."
        )
        create_workspace_files.add_argument(
            "--recursive",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide recursive to create-workspace-file."
        )
        create_workspace_files.add_argument(
            "--root_output_dir",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide root_output_dir to create-workspace-file."
        )
        create_workspace_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_workspace_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_workspace_files = subparser.add_parser(
            'list-workspace-files',
            help='To list all the available Workspace Files.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_workspace_files.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Id to list all the available Workspace Files."
        )
        list_workspace_files.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Name to list all the available Workspace Files."
        )
        list_workspace_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace File Id to list all the available Files."
        )
        list_workspace_files.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace File Path to list all the available Files."
        )
        list_workspace_files.add_argument(
            "--recursive",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide recursive to list files recursively."
        )
        list_workspace_files.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Workspace Files for a specific page_number."
        )
        list_workspace_files.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Workspace Files."
        )
        list_workspace_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_workspace_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_workspace_files = subparser.add_parser(
            'search-workspace-files',
            help='To search all the available Workspace Files.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_workspace_files.add_argument(
            "--file_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide File Name to search all the available Workspace Files."
        )
        search_workspace_files.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Id to search all the available Workspace Files."
        )
        search_workspace_files.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Name to search all the available Workspace Files."
        )
        search_workspace_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace File Id to search all the available Files."
        )
        search_workspace_files.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace File Path to search all the available Files."
        )
        search_workspace_files.add_argument(
            "--recursive",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide recursive to search files recursively."
        )
        search_workspace_files.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Workspace Files for a specific page_number."
        )
        search_workspace_files.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Workspace Files."
        )
        search_workspace_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_workspace_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_workspace_files = subparser.add_parser(
            'get-workspace-file',
            help='To get information about a specific Workspace File.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_workspace_files.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Id to get information about a specific Workspace Files."
        )
        describe_workspace_files.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Name to get information about a specific Workspace Files."
        )
        describe_workspace_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Id to get information about a specific Workspace Files."
        )
        describe_workspace_files.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Path to get information about a specific Workspace Files."
        )
        describe_workspace_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_workspace_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_workspace_files_usage = subparser.add_parser(
            'get-workspace-files-usage',
            help='To get workspace files usage details for a Workspace',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        get_workspace_files_usage.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Id to get workspace files usage details for Workspace."
        )
        get_workspace_files_usage.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Name to get workspace files usage details for Workspace."
        )
        get_workspace_files_usage.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_workspace_files_usage.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_workspace_files = subparser.add_parser(
            'delete-workspace-file',
            help='To delete a specific Workspace File.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_workspace_files.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Id to delete a specific Workspace File."
        )
        delete_workspace_files.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Name to delete a specific Workspace File."
        )
        delete_workspace_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Id to delete a specific Workspace Files."
        )
        delete_workspace_files.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Path to delete a specific Workspace Files."
        )
        delete_workspace_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_workspace_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        download_workspace_files = subparser.add_parser(
            'download-workspace-file',
            help='Download file for a specific workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        download_workspace_files.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Id to download file."
        )
        download_workspace_files.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Name to download file."
        )
        download_workspace_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Id of the file to be downloaded."
        )
        download_workspace_files.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Path of the file to be downloaded."
        )
        download_workspace_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        download_workspace_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
        rename_workspace_file = subparser.add_parser(
            'rename-workspace-file',
            help='To rename a Workspace File or Directory.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        rename_workspace_file.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Id to rename file."
        )
        rename_workspace_file.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Workspace Name to rename file."
        )
        rename_workspace_file.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Id to rename a specific Workspace File."
        )
        rename_workspace_file.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Path of the file to be renamed."
        )
        rename_workspace_file.add_argument(
            "--file_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide the new name for the file."
        )
        rename_workspace_file.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        rename_workspace_file.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
