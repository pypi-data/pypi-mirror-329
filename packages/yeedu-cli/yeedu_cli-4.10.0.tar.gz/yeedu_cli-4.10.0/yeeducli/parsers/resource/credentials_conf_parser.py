from yeeducli.constants import CLOUD_PROVIDERS_LIST
from yeeducli.utility.json_utils import check_non_empty_string, check_boolean, validate_string_and_null
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class CredentialsConfigurationParser:

    def credentials_config_parser(subparser):
        create_credentials_conf = subparser.add_parser(
            'create-credential-conf',
            help='To create a Credential Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_credentials_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create-credential-conf."
        )
        create_credentials_conf.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create-credential-conf."
        )
        create_credentials_conf.add_argument(
            "--credential_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide credential_type_id to create-credential-conf."
        )
        create_credentials_conf.add_argument(
            "--base64_encoded_credentials",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide base64_encoded_credentials to create-credential-conf."
        )
        create_credentials_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_credentials_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_credentials_conf = subparser.add_parser(
            'list-credential-confs',
            help='To list all the Credential Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_credentials_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            choices=CLOUD_PROVIDERS_LIST,
            help="Cloud Provider that will be used for filtering Credential Configurations."
        )
        list_credentials_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Credential Configurations for a specific page_number."
        )
        list_credentials_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Credential Configurations."
        )
        list_credentials_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_credentials_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_credentials_conf = subparser.add_parser(
            'search-credential-confs',
            help='To search all the Credential Configurations based on name.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_credentials_conf.add_argument(
            "--credentials_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide credentials_conf_name to search credential configuration."
        )
        search_credentials_conf.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            choices=CLOUD_PROVIDERS_LIST,
            help="Cloud Provider that will be used for filtering Credential Configurations."
        )
        search_credentials_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Credential Configurations for a specific page_number."
        )
        search_credentials_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Credential Configurations."
        )
        search_credentials_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_credentials_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_credentials_conf = subparser.add_parser(
            'get-credential-conf',
            help='To get the information about a specific Credential Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_credentials_conf.add_argument(
            "--credentials_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide credentials_conf_id to get information about a specific credential configuration."
        )
        describe_credentials_conf.add_argument(
            "--credentials_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide credentials_conf_name to get information about a specific credential configuration."
        )
        describe_credentials_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_credentials_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_credentials_conf = subparser.add_parser(
            'edit-credential-conf',
            help='To edit a specific Credential Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_credentials_conf.add_argument(
            "--credentials_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide credentials_conf_id to edit a specific Credential Configuration."
        )
        edit_credentials_conf.add_argument(
            "--credentials_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide credentials_conf_name to edit a specific Credential Configuration."
        )
        edit_credentials_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to edit-credential-conf."
        )
        edit_credentials_conf.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to edit-credential-conf."
        )
        edit_credentials_conf.add_argument(
            "--base64_encoded_credentials",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide base64_encoded_credentials to edit-credential-conf."
        )
        edit_credentials_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_credentials_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_credentials_conf = subparser.add_parser(
            'delete-credential-conf',
            help='To delete a specific Credential Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_credentials_conf.add_argument(
            "--credentials_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide credentials_conf_id to delete a specific Credential Configuration."
        )
        delete_credentials_conf.add_argument(
            "--credentials_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide credentials_conf_name to delete a specific Credential Configuration."
        )
        delete_credentials_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_credentials_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
