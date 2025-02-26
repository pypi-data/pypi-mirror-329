from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.constants import CLOUD_PROVIDERS_LIST
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null


class CloudEnvironmentParser:

    def cloud_environment_parser(subparser):
        create_cloud_env = subparser.add_parser(
            'create-cloud-env',
            help='To create a cloud environment.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_cloud_env.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create a cloud environment."
        )
        create_cloud_env.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create a cloud environment."
        )
        create_cloud_env.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide cloud_provider_id to create a cloud environment."
        )
        create_cloud_env.add_argument(
            "--availability_zone_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide availability_zone_id to create a cloud environment."
        )
        create_cloud_env.add_argument(
            "--network_conf_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide network_conf_id to create a cloud environment."
        )
        create_cloud_env.add_argument(
            "--cloud_project",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide cloud_project to create a cloud environment."
        )
        create_cloud_env.add_argument(
            "--credential_config_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide credential_config_id to create a cloud environment."
        )
        create_cloud_env.add_argument(
            "--boot_disk_image_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide boot_disk_image_id to create a cloud environment."
        )
        create_cloud_env.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_cloud_env.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_cloud_env = subparser.add_parser(
            'get-cloud-env',
            help='To get detials about a specific cloud environment.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_cloud_env.add_argument(
            "--cloud_env_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cloud_env_id to get detials about a specific cloud environment."
        )
        get_cloud_env.add_argument(
            "--cloud_env_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cloud_env_name to get detials about a specific cloud environment."
        )
        get_cloud_env.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_cloud_env.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_cloud_env = subparser.add_parser(
            'list-cloud-envs',
            help='To list all the available cloud environments.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_cloud_env.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide cloud_provider to list all the related cloud environments of a specific cloud provider."
        )
        list_cloud_env.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list cloud environments for a specific page_number."
        )
        list_cloud_env.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of cloud environments."
        )
        list_cloud_env.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_cloud_env.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_cloud_env = subparser.add_parser(
            'search-cloud-envs',
            help='To search all the available cloud environments.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_cloud_env.add_argument(
            "--cloud_env_name",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide cloud_env_name to search matching cloud environments."
        )
        search_cloud_env.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide cloud_provider to search all the related cloud environments of a specific cloud provider."
        )
        search_cloud_env.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list cloud environments for a specific page_number."
        )
        search_cloud_env.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of cloud environments."
        )
        search_cloud_env.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_cloud_env.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_cloud_env = subparser.add_parser(
            'edit-cloud-env',
            help='To edit a specific cloud environment.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_cloud_env.add_argument(
            "--cloud_env_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cloud_env_id to edit a specific cloud environment."
        )
        edit_cloud_env.add_argument(
            "--cloud_env_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cloud_env_name to edit a specific cloud environment."
        )
        edit_cloud_env.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to edit a specific cloud environment."
        )
        edit_cloud_env.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to edit a specific cloud environment."
        )
        edit_cloud_env.add_argument(
            "--availability_zone_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide availability_zone_id to edit a specific cloud environment."
        )
        edit_cloud_env.add_argument(
            "--network_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide network_conf_id to edit a specific cloud environment."
        )
        edit_cloud_env.add_argument(
            "--cloud_project",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cloud_project to edit a specific cloud environment."
        )
        edit_cloud_env.add_argument(
            "--credential_config_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide credential_config_id to edit a specific cloud environment."
        )
        edit_cloud_env.add_argument(
            "--boot_disk_image_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide boot_disk_image_id to edit a specific cloud environment."
        )
        edit_cloud_env.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_cloud_env.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to edit output in YAML format."
        )

        delete_cloud_env = subparser.add_parser(
            'delete-cloud-env',
            help='To delete a specific cloud environment.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_cloud_env.add_argument(
            "--cloud_env_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cloud_env_id to delete a specific cloud environment."
        )
        delete_cloud_env.add_argument(
            "--cloud_env_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cloud_env_name to delete a specific cloud environment."
        )
        delete_cloud_env.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_cloud_env.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to delete output in YAML format."
        )
