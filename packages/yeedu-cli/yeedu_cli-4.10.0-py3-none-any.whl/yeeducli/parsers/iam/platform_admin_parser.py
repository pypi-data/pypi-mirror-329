from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null


class PlatformAdminParser:

    def tenant_parser(subparser):
        create_tenant = subparser.add_parser(
            'create-tenant',
            help='To create a Tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_tenant.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create-tenant."
        )
        create_tenant.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create-tenant."
        )
        create_tenant.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_tenant.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_tenants = subparser.add_parser(
            'list-tenants',
            help='To list all the available Tenants.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_tenants.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list tenants for a specific page_number."
        )
        list_tenants.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of tenants."
        )
        list_tenants.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_tenants.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_tenant = subparser.add_parser(
            'get-tenant',
            help='To get information about a specific Tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_tenant.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide the tenant_id to get information about a specific Tenant."
        )
        get_tenant.add_argument(
            "--tenant_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide the tenant_name to get information about a specific Tenant."
        )
        get_tenant.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_tenant.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_tenant = subparser.add_parser(
            'delete-tenant',
            help='To delete a specific Tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_tenant.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide the tenant_id to delete a specific Tenant."
        )
        delete_tenant.add_argument(
            "--tenant_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide the tenant_name to delete a specific Tenant."
        )
        delete_tenant.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_tenant.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_tenant = subparser.add_parser(
            'edit-tenant',
            help='To edit a specific Tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_tenant.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific tenant Id to edit-tenant."
        )
        edit_tenant.add_argument(
            "--tenant_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific tenant Name to edit-tenant."
        )
        edit_tenant.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide name to edit-tenant."
        )
        edit_tenant.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide description to edit-tenant."
        )
        edit_tenant.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_tenant.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_tenant = subparser.add_parser(
            'search-tenants',
            help='To search the tenants with the given name.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_tenant.add_argument(
            "--tenant_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide the tenant name to get all the matching tenants."
        )
        search_tenant.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search tenants on a specific page_number."
        )
        search_tenant.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of tenants."
        )
        search_tenant.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_tenant.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

    def platform_admin_parser(subparser):
        list_user_tenants = subparser.add_parser(
            'list-user-tenants',
            help='To list all the tenants associated to an user.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_user_tenants.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to list all the tenants."
        )
        list_user_tenants.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list tenants for a specific page_number."
        )
        list_user_tenants.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of tenants."
        )
        list_user_tenants.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_user_tenants.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
