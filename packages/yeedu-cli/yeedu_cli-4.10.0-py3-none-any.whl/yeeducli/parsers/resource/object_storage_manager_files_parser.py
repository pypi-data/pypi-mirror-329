from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class ObjectStorageManagerFilesParser:

    def object_storage_manager_files_parser(subparser):
        create_object_storage_manager_files = subparser.add_parser(
            'create-object-storage-manager-file',
            help='To create a Object Storage Manager Files.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_object_storage_manager_files.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Id to create-object-storage-manager-file."
        )
        create_object_storage_manager_files.add_argument(
            "--object_storage_manager_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Name to to create-object-storage-manager-file."
        )
        create_object_storage_manager_files.add_argument(
            "--local_file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide local_file_path to create-object-storage-manager-file."
        )
        create_object_storage_manager_files.add_argument(
            "--overwrite",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide overwrite to create-object-storage-manager-file."
        )
        create_object_storage_manager_files.add_argument(
            "--recursive",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide recursive to create-object-storage-manager-file."
        )
        create_object_storage_manager_files.add_argument(
            "--root_output_dir",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide root_output_dir to create-object-storage-manager-file."
        )
        create_object_storage_manager_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_object_storage_manager_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_object_storage_manager_files = subparser.add_parser(
            'list-object-storage-manager-files',
            help='To list all the available Object Storage Manager Files.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_object_storage_manager_files.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Id to list all the available Object Storage Manager Files."
        )
        list_object_storage_manager_files.add_argument(
            "--object_storage_manager_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Name to list all the available Object Storage Manager Files."
        )
        list_object_storage_manager_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager File Id to list all the available Files."
        )
        list_object_storage_manager_files.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager File Path to list all the available Files."
        )
        list_object_storage_manager_files.add_argument(
            "--recursive",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide recursive to list files recursively."
        )
        list_object_storage_manager_files.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Object Storage Manager Files for a specific page_number."
        )
        list_object_storage_manager_files.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Object Storage Manager Files."
        )
        list_object_storage_manager_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_object_storage_manager_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_object_storage_manager_files = subparser.add_parser(
            'search-object-storage-manager-files',
            help='To search all the available Object Storage Manager Files.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_object_storage_manager_files.add_argument(
            "--file_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide File Name to search all the available Object Storage Manager Files."
        )
        search_object_storage_manager_files.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Id to search all the available Object Storage Manager Files."
        )
        search_object_storage_manager_files.add_argument(
            "--object_storage_manager_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Name to search all the available Object Storage Manager Files."
        )
        search_object_storage_manager_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager File Id to search all the available Files."
        )
        search_object_storage_manager_files.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager File Path to search all the available Files."
        )
        search_object_storage_manager_files.add_argument(
            "--recursive",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide recursive to search files recursively."
        )
        search_object_storage_manager_files.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Object Storage Manager Files for a specific page_number."
        )
        search_object_storage_manager_files.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Object Storage Manager Files."
        )
        search_object_storage_manager_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_object_storage_manager_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_object_storage_manager_files = subparser.add_parser(
            'get-object-storage-manager-file',
            help='To get information about a specific Object Storage Manager File.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_object_storage_manager_files.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Id to get information about a specific Object Storage Manager Files."
        )
        describe_object_storage_manager_files.add_argument(
            "--object_storage_manager_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Name to get information about a specific Object Storage Manager Files."
        )
        describe_object_storage_manager_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Id to get information about a specific Object Storage Manager Files."
        )
        describe_object_storage_manager_files.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Path to get information about a specific Object Storage Manager Files."
        )
        describe_object_storage_manager_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_object_storage_manager_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_object_storage_manager_files = subparser.add_parser(
            'delete-object-storage-manager-file',
            help='To delete a specific Object Storage Manager File.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_object_storage_manager_files.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Id to delete a specific Object Storage Manager File."
        )
        delete_object_storage_manager_files.add_argument(
            "--object_storage_manager_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Name to delete a specific Object Storage Manager File."
        )
        delete_object_storage_manager_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Id to delete a specific Object Storage Manager Files."
        )
        delete_object_storage_manager_files.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Path to delete a specific Object Storage Manager Files."
        )
        delete_object_storage_manager_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_object_storage_manager_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
        
        download_object_storage_manager_files = subparser.add_parser(
            'download-object-storage-manager-file',
            help='Download file for a specific object storage manager.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        download_object_storage_manager_files.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Id to download file."
        )
        download_object_storage_manager_files.add_argument(
            "--object_storage_manager_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Name to download file."
        )
        download_object_storage_manager_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Id of the file to be downloaded."
        )
        download_object_storage_manager_files.add_argument(
            "--file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide File Path of the file to be downloaded."
        )
        download_object_storage_manager_files.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        download_object_storage_manager_files.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
