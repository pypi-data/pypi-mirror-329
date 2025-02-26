from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.constants import CLOUD_PROVIDERS_LIST
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null


class BootDiskImageConfigurationParser:

    def boot_disk_image_config_parser(subparser):
        create_boot_disk_image_conf = subparser.add_parser(
            'create-boot-disk-image-conf',
            help='To create a boot disk image configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_boot_disk_image_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create-boot-disk-image-conf."
        )
        create_boot_disk_image_conf.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create-boot-disk-image-conf."
        )
        create_boot_disk_image_conf.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide cloud_provider_id to create-boot-disk-image-conf."
        )
        create_boot_disk_image_conf.add_argument(
            "--linux_distro_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide linux_distro_id to create-boot-disk-image-conf."
        )
        create_boot_disk_image_conf.add_argument(
            "--boot_disk_image",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide boot_disk_image to create-boot-disk-image-conf."
        )
        create_boot_disk_image_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_boot_disk_image_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_boot_disk_image_conf = subparser.add_parser(
            'get-boot-disk-image-conf',
            help='To get the information about a specific boot disk image configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_boot_disk_image_conf.add_argument(
            "--boot_disk_image_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Boot Disk Image Id to get information about a specific boot disk image configuration."
        )
        describe_boot_disk_image_conf.add_argument(
            "--boot_disk_image_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Boot Disk Image Name to get information about a specific boot disk image configuration."
        )
        describe_boot_disk_image_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_boot_disk_image_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_boot_disk_image_conf = subparser.add_parser(
            'list-boot-disk-image-confs',
            help='To list all the available boot disk image configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_boot_disk_image_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide cloud_provider to list all the related boot disk image configs for a specific Cloud Provider."
        )
        list_boot_disk_image_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list boot disk image configurations for a specific page_number."
        )
        list_boot_disk_image_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of boot disk image configurations."
        )
        list_boot_disk_image_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_boot_disk_image_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_boot_disk_image_conf = subparser.add_parser(
            'search-boot-disk-image-confs',
            help='To search all the available boot disk image configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_boot_disk_image_conf.add_argument(
            "--boot_disk_image_name",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Boot Disk Image Name to search information about all the related boot disk image configs."
        )
        search_boot_disk_image_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide cloud_provider to search all the related boot disk image configs for a specific Cloud Provider."
        )
        search_boot_disk_image_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list boot disk image configurations for a specific page_number."
        )
        search_boot_disk_image_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of boot disk image configurations."
        )
        search_boot_disk_image_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_boot_disk_image_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_boot_disk_image_conf = subparser.add_parser(
            'edit-boot-disk-image-conf',
            help='To edit a specific boot disk image configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_boot_disk_image_conf.add_argument(
            "--boot_disk_image_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide boot_disk_image_id to edit a specific boot disk image configuration."
        )
        edit_boot_disk_image_conf.add_argument(
            "--boot_disk_image_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide boot_disk_image_name to edit a specific boot disk image configuration."
        )
        edit_boot_disk_image_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to edit a specific boot disk image configuration."
        )
        edit_boot_disk_image_conf.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to edit a specific boot disk image configuration."
        )
        edit_boot_disk_image_conf.add_argument(
            "--linux_distro_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide linux_distro_id to edit a specific boot disk image configuration."
        )
        edit_boot_disk_image_conf.add_argument(
            "--boot_disk_image",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide boot_disk_image to edit a specific boot disk image configuration."
        )
        edit_boot_disk_image_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_boot_disk_image_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to edit output in YAML format."
        )

        delete_boot_disk_image_conf = subparser.add_parser(
            'delete-boot-disk-image-conf',
            help='To delete a specific boot disk image configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_boot_disk_image_conf.add_argument(
            "--boot_disk_image_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide boot_disk_image_id to delete a specific boot disk image configuration."
        )
        delete_boot_disk_image_conf.add_argument(
            "--boot_disk_image_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide boot_disk_image_name to delete a specific boot disk image configuration."
        )
        delete_boot_disk_image_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_boot_disk_image_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to delete output in YAML format."
        )
