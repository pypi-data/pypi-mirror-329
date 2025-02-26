from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.constants import CLOUD_PROVIDERS_LIST
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null


class NetworkConfigurationParser:

    def network_configuration_parser(subparser):
        create_network_conf = subparser.add_parser(
            'create-network-conf',
            help='To create the Network Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_network_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create-network-conf."
        )
        create_network_conf.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create-network-conf."
        )
        create_network_conf.add_argument(
            "--network_project_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide network_project_id to create-network-conf."
        )
        create_network_conf.add_argument(
            "--network_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide network_name to create-network-conf."
        )
        create_network_conf.add_argument(
            "--subnet",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide subnet to create-network-conf."
        )
        create_network_conf.add_argument(
            "--availability_zone_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide availability_zone_id to create-network-conf."
        )
        create_network_conf.add_argument(
            "--network_tags",
            type=check_non_empty_string,
            metavar=['value1,value2'],
            default=[],
            help="Provide network_tags to create-network-conf."
        )
        create_network_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_network_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_network_conf = subparser.add_parser(
            'list-network-confs',
            help='To get information about Network Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_network_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide specific cloud_provider to get information about related Network Configurations."
        )
        list_network_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Network Configurations for a specific page_number."
        )
        list_network_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Network Configurations."
        )
        list_network_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_network_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_network_conf = subparser.add_parser(
            'search-network-confs',
            help='To search information about Network Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_network_conf.add_argument(
            "--network_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide network_conf_name to search Network Configuration."
        )
        search_network_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide specific cloud_provider to search about related Network Configurations."
        )
        search_network_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Network Configurations for a specific page_number."
        )
        search_network_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Network Configurations."
        )
        search_network_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_network_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_network_conf = subparser.add_parser(
            'get-network-conf',
            help='To get information about a specific Network Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_network_conf.add_argument(
            "--network_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide network_conf_id to get information about a specific network Configuration."
        )
        describe_network_conf.add_argument(
            "--network_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide network_conf_name to get information about a specific network Configuration."
        )
        describe_network_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_network_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_network_conf = subparser.add_parser(
            'edit-network-conf',
            help='To edit a specific Network Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_network_conf.add_argument(
            "--network_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific Network Configuration network_conf_id to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--network_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific Network Configuration network_conf_name to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--network_name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide network_name to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--network_project_id",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide network_project_id to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--availability_zone_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide availability_zone_id to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--subnet",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide subnet to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--network_tags",
            type=check_non_empty_string,
            default=SUPPRESS,
            metavar=['value1,value2'],
            help="Provide network_tags to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_network_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_network_conf = subparser.add_parser(
            'delete-network-conf',
            help='To delete a specific Network Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_network_conf.add_argument(
            "--network_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide network_conf_id to delete a specific network Configuration."
        )
        delete_network_conf.add_argument(
            "--network_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide network_conf_name to delete a specific network Configuration."
        )
        delete_network_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_network_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
