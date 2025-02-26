from yeeducli.constants import CLOUD_PROVIDERS_LIST, COMPUTE_TYPES_LIST
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null, validate_integer_and_null
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class ClusterConfigurationParser:

    def cluster_configuration_parser(subparser):

        create_cluster_conf = subparser.add_parser(
            'create-conf',
            help='Create a new cluster configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_cluster_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Assigns a name to the cluster configuration."
        )
        create_cluster_conf.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provides a description for the cluster configuration."
        )
        create_cluster_conf.add_argument(
            "--machine_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Sets the machine type ID for the cluster configuration."
        )
        create_cluster_conf.add_argument(
            "--volume_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Sets the volume configuration ID for the cluster configuration."
        )
        create_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_cluster_conf = subparser.add_parser(
            'list-confs',
            help='List all the cluster configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        list_cluster_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Specifies the cloud provider to filter the cluster configurations."
        )
        list_cluster_conf.add_argument(
            "--compute_type",
            type=check_non_empty_string,
            nargs='?',
            choices=COMPUTE_TYPES_LIST,
            default=SUPPRESS,
            help="Specifies the compute type to filter the cluster configurations."
        )
        list_cluster_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Specifies the page number for results pagination."
        )
        list_cluster_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Specifies the maximum number of configurations to list per page."
        )
        list_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_cluster_conf = subparser.add_parser(
            'search-confs',
            help='Search cluster configurations based on configuration name.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        search_cluster_conf.add_argument(
            "--cluster_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Specifies the name of the cluster configuration to search for."
        )
        search_cluster_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Specifies the cloud provider to filter the cluster configurations."
        )
        search_cluster_conf.add_argument(
            "--compute_type",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            choices=COMPUTE_TYPES_LIST,
            help="Specifies the compute type to filter the cluster configurations."
        )
        search_cluster_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Specifies the page number for results pagination."
        )
        search_cluster_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Specifies the maximum number of configurations to search per page."
        )
        search_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_cluster_conf = subparser.add_parser(
            'get-conf',
            help='Get details of a specific cluster configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_cluster_conf.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the ID of the cluster configuration to retrieve details."
        )
        get_cluster_conf.add_argument(
            "--cluster_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the name of the cluster configuration to retrieve details."
        )
        get_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_cluster_conf = subparser.add_parser(
            'edit-conf',
            help='Modify details of a specific cluster configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_cluster_conf.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the ID of the cluster configuration to edit."
        )
        edit_cluster_conf.add_argument(
            "--cluster_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the name of the cluster configuration to edit."
        )
        edit_cluster_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Assigns a new name to the cluster configuration."
        )
        edit_cluster_conf.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provides a new description for the cluster configuration."
        )
        edit_cluster_conf.add_argument(
            "--machine_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Sets a new machine type ID for the cluster configuration."
        )
        edit_cluster_conf.add_argument(
            "--volume_conf_id",
            type=validate_integer_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Sets a new volume configuration ID for the cluster configuration."
        )
        edit_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_cluster_conf = subparser.add_parser(
            'delete-conf',
            help='Delete a specific cluster configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_cluster_conf.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the ID of the cluster configuration to delete."
        )
        delete_cluster_conf.add_argument(
            "--cluster_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the name of the cluster configuration to delete."
        )
        delete_cluster_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_cluster_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
