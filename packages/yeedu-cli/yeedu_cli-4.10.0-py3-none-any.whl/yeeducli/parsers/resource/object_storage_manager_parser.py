from yeeducli.constants import CLOUD_PROVIDERS_LIST
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null


class ObjectStorageManagerParser:

    def object_storage_manager_parser(subparser):
        create_object_storage_manager_conf = subparser.add_parser(
            'create-object-storage-manager',
            help='To create a Object Storage Manager.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_object_storage_manager_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create-object-storage-manager."
        )
        create_object_storage_manager_conf.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create-object-storage-manager."
        )
        create_object_storage_manager_conf.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide cloud_provider_id to create-object-storage-manager."
        )
        create_object_storage_manager_conf.add_argument(
            "--credentials_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide credentials_conf_id to create-object-storage-manager."
        )
        create_object_storage_manager_conf.add_argument(
            "--object_storage_bucket_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide object_storage_bucket_name to create-object-storage-manager."
        )
        create_object_storage_manager_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_object_storage_manager_conf = subparser.add_parser(
            'get-object-storage-manager',
            help='To get information about a specific Object Storage Manager.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_object_storage_manager_conf.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Id to get information about a specific Object Storage Manager."
        )
        describe_object_storage_manager_conf.add_argument(
            "--object_storage_manager_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Object Storage Manager Name to get information about a specific Object Storage Manager."
        )
        describe_object_storage_manager_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_object_storage_manager_conf = subparser.add_parser(
            'list-object-storage-managers',
            help='To list all the available  Object Storage Manager Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_object_storage_manager_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            choices=CLOUD_PROVIDERS_LIST,
            help="Cloud Provider that will be used for filtering list."
        )
        list_object_storage_manager_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Object Storage Managers for a specific page_number."
        )
        list_object_storage_manager_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Object Storage Managers."
        )
        list_object_storage_manager_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_object_storage_manager_conf = subparser.add_parser(
            'search-object-storage-managers',
            help='To search Object Storage Manager Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_object_storage_manager_conf.add_argument(
            "--object_storage_manager_name",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Object Storage Manager Name to search information about a specific Object Storage Manager."
        )
        search_object_storage_manager_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            choices=CLOUD_PROVIDERS_LIST,
            help="Cloud Provider that will be used for filtering list."
        )
        search_object_storage_manager_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Object Storage Managers for a specific page_number."
        )
        search_object_storage_manager_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Object Storage Managers."
        )
        search_object_storage_manager_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_object_storage_manager_conf = subparser.add_parser(
            'edit-object-storage-manager',
            help='To edit a specific Object Storage Manager Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_object_storage_manager_conf.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide object_storage_manager_id to edit information about a specific Object Storage Manager."
        )
        edit_object_storage_manager_conf.add_argument(
            "--object_storage_manager_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide object_storage_manager_name to edit information about a specific Object Storage Manager."
        )
        edit_object_storage_manager_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to edit-object-storage-manager."
        )
        edit_object_storage_manager_conf.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to edit-object-storage-manager."
        )
        edit_object_storage_manager_conf.add_argument(
            "--credentials_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide credentials_conf_id to edit-object-storage-manager."
        )
        edit_object_storage_manager_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_object_storage_manager_conf = subparser.add_parser(
            'delete-object-storage-manager',
            help='To delete a specific Object Storage Manager.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_object_storage_manager_conf.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide object_storage_manager_id to delete a specific Object Storage Manager."
        )
        delete_object_storage_manager_conf.add_argument(
            "--object_storage_manager_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide object_storage_manager_name to delete a specific Object Storage Manager."
        )
        delete_object_storage_manager_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
