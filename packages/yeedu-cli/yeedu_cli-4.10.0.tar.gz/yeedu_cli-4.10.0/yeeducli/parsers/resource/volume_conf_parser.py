from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.constants import CLOUD_PROVIDERS_LIST
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null, validate_integer_and_null


class VolumeConfigurationParser:

    def volume_configuration_parser(subparser):
        create_volume_conf = subparser.add_parser(
            'create-volume-conf',
            help='To create the Volume Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_volume_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            required=True,
            help="Provide name to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide description to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--encrypted",
            type=check_boolean,
            nargs=1,
            default=SUPPRESS,
            choices=['true', 'false'],
            required=True,
            help="Provide encrypted to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--size",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide size to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--disk_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide disk_type to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--machine_volume_num",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide machine_volume_num to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--machine_volume_strip_num",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide machine_volume_strip_num to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--disk_iops",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide disk_iops to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--disk_throughput_MB",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide disk_throughput_MB to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_volume_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_volume_conf = subparser.add_parser(
            'get-volume-conf',
            help='To get information about a specific Volume Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_volume_conf.add_argument(
            "--volume_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide volume_conf_id to get information about a specific Volume Configuration."
        )
        describe_volume_conf.add_argument(
            "--volume_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide volume_conf_name to get information about a specific Volume Configuration."
        )
        describe_volume_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_volume_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_volume_conf = subparser.add_parser(
            'list-volume-confs',
            help='To list all the available Volume Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_volume_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="To list volume configurations for a specific cloud provider."
        )
        list_volume_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Volume Configurations for a specific page_number."
        )
        list_volume_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Volume Configurations."
        )
        list_volume_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_volume_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_volume_conf = subparser.add_parser(
            'search-volume-confs',
            help='To search all the available Volume Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_volume_conf.add_argument(
            "--volume_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide volume_conf_name to search all the available Volume Configurations."
        )
        search_volume_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="To search volume configurations for a specific cloud provider."
        )
        search_volume_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Volume Configurations for a specific page_number."
        )
        search_volume_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Volume Configurations."
        )
        search_volume_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_volume_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_volume_conf = subparser.add_parser(
            'edit-volume-conf',
            help='To edit a specific Volume Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_volume_conf.add_argument(
            "--volume_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide specific volume_conf_id to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--volume_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide specific volume_conf_name to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide name to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide description to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--encrypted",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide encrypted to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--disk_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide disk_type to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--size",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide size to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--machine_volume_num",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide machine_volume_num to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--machine_volume_strip_num",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide machine_volume_strip_num to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--disk_iops",
            type=validate_integer_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide disk_iops to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--disk_throughput_MB",
            type=validate_integer_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide disk_throughput_MB to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_volume_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_volume_conf = subparser.add_parser(
            'delete-volume-conf',
            help='To delete a specific Volume Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_volume_conf.add_argument(
            "--volume_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide volume_conf_id to delete a specific Volume Configuration."
        )
        delete_volume_conf.add_argument(
            "--volume_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide volume_conf_name to delete a specific Volume Configuration."
        )
        delete_volume_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_volume_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
