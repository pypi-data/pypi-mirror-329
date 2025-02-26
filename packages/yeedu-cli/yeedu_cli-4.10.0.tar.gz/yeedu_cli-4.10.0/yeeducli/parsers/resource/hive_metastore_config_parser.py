from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null


class HiveMetastoreConfigParser:

    def hive_metastore_config_parser(subparser):
        create_hive_metastore_config = subparser.add_parser(
            'create-hive-metastore-conf',
            help='To create a Hive Metastore Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_hive_metastore_config.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create-hive-metastore-conf."
        )
        create_hive_metastore_config.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create-hive-metastore-conf."
        )
        create_hive_metastore_config.add_argument(
            "--hive_site_xml_file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide hive_site_xml_file_path to create-hive-metastore-conf."
        )
        create_hive_metastore_config.add_argument(
            "--core_site_xml_file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide core_site_xml_file_path to create-hive-metastore-conf."
        )
        create_hive_metastore_config.add_argument(
            "--hdfs_site_xml_file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide hdfs_site_xml_file_path to create-hive-metastore-conf."
        )
        create_hive_metastore_config.add_argument(
            "--krb5_conf_file_path",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide krb5_conf_file_path to create-hive-metastore-conf."
        )
        create_hive_metastore_config.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_hive_metastore_config.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_hive_metastore_config = subparser.add_parser(
            'list-hive-metastore-confs',
            help='To list all the available Hive Metastore Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_hive_metastore_config.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Hive Metastore Configurations for a specific page_number."
        )
        list_hive_metastore_config.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Hive Metastore Configurations."
        )
        list_hive_metastore_config.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_hive_metastore_config.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_hive_metastore_config = subparser.add_parser(
            'search-hive-metastore-confs',
            help='To search all the available Hive Metastore Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_hive_metastore_config.add_argument(
            "--hive_metastore_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide hive_metastore_conf_name to search information about Hive Metastore Configurations."
        )
        search_hive_metastore_config.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Hive Metastore Configurations for a specific page_number."
        )
        search_hive_metastore_config.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Hive Metastore Configurations."
        )
        search_hive_metastore_config.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_hive_metastore_config.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_hive_metastore_config = subparser.add_parser(
            'get-hive-metastore-conf',
            help='To get the information about a specific Hive Metastore Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_hive_metastore_config.add_argument(
            "--hive_metastore_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide hive_metastore_conf_id to get information about a specific Hive Metastore Configuration."
        )
        describe_hive_metastore_config.add_argument(
            "--hive_metastore_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide hive_metastore_conf_name to get information about a specific Hive Metastore Configuration."
        )
        describe_hive_metastore_config.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_hive_metastore_config.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_hive_metastore_config = subparser.add_parser(
            'edit-hive-metastore-conf',
            help='To edit a specific Hive Metastore Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_hive_metastore_config.add_argument(
            "--hive_metastore_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific hive_metastore_conf_id to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--hive_metastore_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific hive_metastore_conf_name to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--hive_site_xml_file_path",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide hive_site_xml_file_path to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--core_site_xml_file_path",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide core_site_xml_file_path to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--hdfs_site_xml_file_path",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide hdfs_site_xml_file_path to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--krb5_conf_file_path",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide krb5_conf_file_path to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_hive_metastore_config.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_hive_metastore_config = subparser.add_parser(
            'delete-hive-metastore-conf',
            help='To delete a specific Hive Metastore Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_hive_metastore_config.add_argument(
            "--hive_metastore_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide hive_metastore_conf_id to delete a specific Hive Metastore Configuration."
        )
        delete_hive_metastore_config.add_argument(
            "--hive_metastore_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide hive_metastore_conf_name to delete a specific Hive Metastore Configuration."
        )
        delete_hive_metastore_config.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_hive_metastore_config.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
