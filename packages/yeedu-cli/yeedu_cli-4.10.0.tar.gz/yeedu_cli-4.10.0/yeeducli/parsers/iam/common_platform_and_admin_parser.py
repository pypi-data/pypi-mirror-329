from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class CommonPlatformAndAdminParser:

    def admin_parser(subparser):
        list_users = subparser.add_parser(
            'list-users',
            help='To list all the users present in tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users for a specific page_number."
        )
        list_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users."
        )
        list_users.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_users.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_users = subparser.add_parser(
            'search-users',
            help='To search all the users present in tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_users.add_argument(
            "--username",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide username to search matching users."
        )
        search_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search users for a specific page_number."
        )
        search_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of users."
        )
        search_users.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_users.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_user = subparser.add_parser(
            'get-user',
            help='To get information about a specific User.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_user.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to get information about a specific User."
        )
        get_user.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_user.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_user_roles = subparser.add_parser(
            'get-user-roles',
            help='To get all the roles of a specific User.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_user_roles.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to get roles of a specific User."
        )
        get_user_roles.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_user_roles.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_user_roles = subparser.add_parser(
            'list-users-roles',
            help='To list all the Users Roles.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_user_roles.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users roles for a specific page_number."
        )
        list_user_roles.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users roles."
        )
        list_user_roles.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_user_roles.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_role_users = subparser.add_parser(
            'get-role-users',
            help='To get all the users having a specific role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_role_users.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide role id to get users in a specific role."
        )
        get_role_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users for a specific page_number."
        )
        get_role_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users."
        )
        get_role_users.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_role_users.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_groups = subparser.add_parser(
            'list-groups',
            help='To list all the groups present in tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups for a specific page_number."
        )
        list_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups."
        )
        list_groups.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_groups.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_groups = subparser.add_parser(
            'search-groups',
            help='To search all the groups present in tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_groups.add_argument(
            "--groupname",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide groupname to search matching groups."
        )
        search_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search groups for a specific page_number."
        )
        search_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of groups."
        )
        search_groups.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_groups.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_group = subparser.add_parser(
            'get-group',
            help='To get information about a specific Group.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_group.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to get information about a specific Group."
        )
        get_group.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_group.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_group_roles = subparser.add_parser(
            'get-group-roles',
            help='To get all the roles of a specific Group.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_group_roles.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to get roles of a specific Group."
        )
        get_group_roles.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_group_roles.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_group_roles = subparser.add_parser(
            'list-groups-roles',
            help='To list all the Groups Roles.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_group_roles.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups roles for a specific page_number."
        )
        list_group_roles.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups roles."
        )
        list_group_roles.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_group_roles.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_role_groups = subparser.add_parser(
            'get-role-groups',
            help='To get all the groups having a specific role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_role_groups.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide role id to get groups in a specific role."
        )
        get_role_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups for a specific page_number."
        )
        get_role_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups."
        )
        get_role_groups.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_role_groups.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        create_user_role = subparser.add_parser(
            'create-user-role',
            help='To create an User Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_user_role.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to create-user-role."
        )
        create_user_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to create-user-role."
        )
        create_user_role.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_user_role.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_user_role = subparser.add_parser(
            'delete-user-role',
            help='To delete an User Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_user_role.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to delete-user-role."
        )
        delete_user_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to delete-user-role."
        )
        delete_user_role.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_user_role.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        create_group_role = subparser.add_parser(
            'create-group-role',
            help='To create a Group Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_group_role.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to create-group-role."
        )
        create_group_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to create-group-role."
        )
        create_group_role.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_group_role.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_group_role = subparser.add_parser(
            'delete-group-role',
            help='To delete a group Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_group_role.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to delete-group-role."
        )
        delete_group_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to delete-group-role."
        )
        delete_group_role.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_group_role.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

    def platform_admin_parser(subparser):
        list_tenant_users = subparser.add_parser(
            'list-tenant-users',
            help='To list all the users present in a tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_tenant_users.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Tenant Id to list all the users present in it."
        )
        list_tenant_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list tenant users for a specific page_number."
        )
        list_tenant_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of tenant users."
        )
        list_tenant_users.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_tenant_users.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_tenant_users = subparser.add_parser(
            'search-tenant-users',
            help='To search all the users present in a tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_tenant_users.add_argument(
            "--username",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide username to search all the matching users present in it."
        )
        search_tenant_users.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Tenant Id to search all the users present in it."
        )
        search_tenant_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search tenant users for a specific page_number."
        )
        search_tenant_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of tenant users."
        )
        search_tenant_users.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_tenant_users.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_tenant_user = subparser.add_parser(
            'get-tenant-user',
            help='To get information about a User present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_tenant_user.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Tenant Id to get information about a specific User."
        )
        get_tenant_user.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to get information about a specific User."
        )
        get_tenant_user.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_tenant_user.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_user_roles = subparser.add_parser(
            'get-user-roles',
            help='To get all the roles of an User present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_user_roles.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Tenant Id to get roles of a specific User."
        )
        get_user_roles.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to get roles of a specific User."
        )
        get_user_roles.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_user_roles.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_user_roles = subparser.add_parser(
            'list-users-roles',
            help='To list all the Users Roles in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_user_roles.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Tenant Id to list User roles."
        )
        list_user_roles.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users roles for a specific page_number."
        )
        list_user_roles.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users roles."
        )
        list_user_roles.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_user_roles.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_role_users = subparser.add_parser(
            'get-role-users',
            help='To get all the users having a specific role in a tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_role_users.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide tenant id to get users in a specific role."
        )
        get_role_users.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide role id to get users in a specific role."
        )
        get_role_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users for a specific page_number."
        )
        get_role_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users."
        )
        get_role_users.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_role_users.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_tenant_groups = subparser.add_parser(
            'list-tenant-groups',
            help='To list all the groups present in a tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_tenant_groups.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Tenant Id to list all the groups present in it."
        )
        list_tenant_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list tenant groups for a specific page_number."
        )
        list_tenant_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of tenant groups."
        )
        list_tenant_groups.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_tenant_groups.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_tenant_groups = subparser.add_parser(
            'search-tenant-groups',
            help='To search all the groups present in a tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_tenant_groups.add_argument(
            "--groupname",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide groupname to search all the matching groups present in it."
        )
        search_tenant_groups.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Tenant Id to search all the groups present in it."
        )
        search_tenant_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search tenant groups for a specific page_number."
        )
        search_tenant_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of tenant groups."
        )
        search_tenant_groups.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_tenant_groups.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_tenant_group = subparser.add_parser(
            'get-tenant-group',
            help='To get information about a Group present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_tenant_group.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Tenant Id to get information about a specific Group."
        )
        get_tenant_group.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to get information about a specific Group."
        )
        get_tenant_group.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_tenant_group.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_group_roles = subparser.add_parser(
            'get-group-roles',
            help='To get all the roles of a Group present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_group_roles.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Tenant Id to get roles of a specific Group."
        )
        get_group_roles.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to get roles of a specific Group."
        )
        get_group_roles.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_group_roles.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_group_roles = subparser.add_parser(
            'list-groups-roles',
            help='To list all the Groups Roles in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_group_roles.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Tenant Id to list Group roles."
        )
        list_group_roles.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups roles for a specific page_number."
        )
        list_group_roles.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups roles."
        )
        list_group_roles.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_group_roles.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_role_groups = subparser.add_parser(
            'get-role-groups',
            help='To get all the groups having a specific Role present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_role_groups.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide tenant id to get groups in a specific role."
        )
        get_role_groups.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide role id to get groups in a specific role."
        )
        get_role_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups for a specific page_number."
        )
        get_role_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups."
        )
        get_role_groups.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_role_groups.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        create_user_role = subparser.add_parser(
            'create-user-role',
            help='To create an User Role for a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_user_role.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Tenant Id to create-user-role."
        )
        create_user_role.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to create-user-role."
        )
        create_user_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to create-user-role."
        )
        create_user_role.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_user_role.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_user_role = subparser.add_parser(
            'delete-user-role',
            help='To delete an User Role of a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_user_role.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Tenant Id to delete-user-role."
        )
        delete_user_role.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to delete-user-role."
        )
        delete_user_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to delete-user-role."
        )
        delete_user_role.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_user_role.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        create_group_role = subparser.add_parser(
            'create-group-role',
            help='To create a Group Role for a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_group_role.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Tenant Id to create-group-role."
        )
        create_group_role.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to create-group-role."
        )
        create_group_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to create-group-role."
        )
        create_group_role.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_group_role.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_group_role = subparser.add_parser(
            'delete-group-role',
            help='To delete a Group Role of a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_group_role.add_argument(
            "--tenant_id",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Tenant Id to delete-group-role."
        )
        delete_group_role.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to delete-group-role."
        )
        delete_group_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to delete-group-role."
        )
        delete_group_role.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_group_role.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
