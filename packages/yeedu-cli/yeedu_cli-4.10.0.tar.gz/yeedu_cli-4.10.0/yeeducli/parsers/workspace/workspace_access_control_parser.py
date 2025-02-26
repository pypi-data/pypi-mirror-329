from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class WorkspaceAccessControlParser:
    def workspace_access_control_parser(subparser):
        create_workspace_user_access = subparser.add_parser(
            'create-user-access',
            help='Assign access to a user on a specific workspace',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_workspace_user_access.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to assign user access on a workspace."
        )
        create_workspace_user_access.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to assign user access on a workspace."
        )
        create_workspace_user_access.add_argument(
            "--permission_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Permission Id to assign user access on a workspace."
        )
        create_workspace_user_access.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_workspace_user_access.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        create_workspace_group_access = subparser.add_parser(
            'create-group-access',
            help='Assign access to a group on a specific workspace',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_workspace_group_access.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to assign group access on a workspace."
        )
        create_workspace_group_access.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide group Id to assign group access on a workspace."
        )
        create_workspace_group_access.add_argument(
            "--permission_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Permission Id to assign group access on a workspace."
        )
        create_workspace_group_access.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_workspace_group_access.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_workspace_user_access = subparser.add_parser(
            'delete-user-access',
            help='Delete access of a user on a specific workspace',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_workspace_user_access.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to delete user access on a workspace."
        )
        delete_workspace_user_access.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to delete user access on a workspace."
        )
        delete_workspace_user_access.add_argument(
            "--permission_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Permission Id to delete user access on a workspace."
        )
        delete_workspace_user_access.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_workspace_user_access.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_workspace_group_access = subparser.add_parser(
            'delete-group-access',
            help='Delete access of a group on a specific workspace',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_workspace_group_access.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to delete group access on a workspace."
        )
        delete_workspace_group_access.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide group Id to delete group access on a workspace."
        )
        delete_workspace_group_access.add_argument(
            "--permission_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Permission Id to delete group access on a workspace."
        )
        delete_workspace_group_access.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_workspace_group_access.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_workspace_users = subparser.add_parser(
            'list-users',
            help='To list users who have no permissions in a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_workspace_users.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to list all the users."
        )
        list_workspace_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users for a specific page_number."
        )
        list_workspace_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users."
        )
        list_workspace_users.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_workspace_users.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_workspace_user_access = subparser.add_parser(
            'get-user-access',
            help='To get the permission of the user having access to a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_workspace_user_access.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to get the permission of a user."
        )
        get_workspace_user_access.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to get the permission of a user."
        )
        get_workspace_user_access.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_workspace_user_access.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_workspace_users_access = subparser.add_parser(
            'list-users-access',
            help='To list all the users of specific permission having access to a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_workspace_users_access.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Specifies the ID of the workspace to retrieve users from."
        )
        list_workspace_users_access.add_argument(
            "--permission_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the ID of the permission to retrieve users."
        )
        list_workspace_users_access.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users for a specific page_number."
        )
        list_workspace_users_access.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users."
        )
        list_workspace_users_access.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_workspace_users_access.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
        
        search_workspace_users_access = subparser.add_parser(
            'search-users-access',
            help='To search all the users for the provided username having access to a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_workspace_users_access.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Specifies the ID of the workspace to search users from."
        )
        search_workspace_users_access.add_argument(
            "--username",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Specifies username to retrieve users."
        )
        search_workspace_users_access.add_argument(
            "--permission_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the ID of the permission to retrieve users."
        )
        search_workspace_users_access.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users for a specific page_number."
        )
        search_workspace_users_access.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users."
        )
        search_workspace_users_access.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_workspace_users_access.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_workspace_users = subparser.add_parser(
            'search-users',
            help='To search for users by username who have no permissions in a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_workspace_users.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to search all the users."
        )
        search_workspace_users.add_argument(
            "--username",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide username to search all the users."
        )
        search_workspace_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search users for a specific page_number."
        )
        search_workspace_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of users."
        )
        search_workspace_users.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_workspace_users.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        match_workspace_user = subparser.add_parser(
            'match-user',
            help='To match a user by username having access to a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        match_workspace_user.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to match all the users."
        )
        match_workspace_user.add_argument(
            "--username",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide username to match all the users."
        )
        match_workspace_user.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        match_workspace_user.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_workspace_groups = subparser.add_parser(
            'list-groups',
            help='To list groups who have no permissions in a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_workspace_groups.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to list all the groups."
        )
        list_workspace_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups for a specific page_number."
        )
        list_workspace_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups."
        )
        list_workspace_groups.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_workspace_groups.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_workspace_group_access = subparser.add_parser(
            'get-group-access',
            help='To get the permission of a group having access to a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_workspace_group_access.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Workspace Id to get the permission of a group."
        )
        get_workspace_group_access.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Group Id to get the permission of a group."
        )
        get_workspace_group_access.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_workspace_group_access.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_workspace_groups_access = subparser.add_parser(
            'list-groups-access',
            help='To list all the groups of specific permission having access to a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_workspace_groups_access.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Specifies the ID of the workspace to list groups from."
        )
        list_workspace_groups_access.add_argument(
            "--permission_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the ID of the permission to retrieve groups."
        )
        list_workspace_groups_access.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups for a specific page_number."
        )
        list_workspace_groups_access.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups."
        )
        list_workspace_groups_access.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_workspace_groups_access.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
        
        search_workspace_groups_access = subparser.add_parser(
            'search-groups-access',
            help='To search all the groups for the provided groupname having access to a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_workspace_groups_access.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Specifies the ID of the workspace to search groups from."
        )
        search_workspace_groups_access.add_argument(
            "--groupname",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Specifies groupname to retrieve groups."
        )
        search_workspace_groups_access.add_argument(
            "--permission_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Specifies the ID of the permission to retrieve groups."
        )
        search_workspace_groups_access.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups for a specific page_number."
        )
        search_workspace_groups_access.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups."
        )
        search_workspace_groups_access.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_workspace_groups_access.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_workspace_groups = subparser.add_parser(
            'search-groups',
            help='To search for groups by groupname who have no permissions in a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_workspace_groups.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to search all the groups."
        )
        search_workspace_groups.add_argument(
            "--groupname",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide groupname to search all the groups."
        )
        search_workspace_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search groups for a specific page_number."
        )
        search_workspace_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of groups."
        )
        search_workspace_groups.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_workspace_groups.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        match_workspace_group = subparser.add_parser(
            'match-group',
            help='To match a group by groupname having access to a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        match_workspace_group.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to match all the groups."
        )
        match_workspace_group.add_argument(
            "--groupname",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide groupname to match all the groups."
        )
        match_workspace_group.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        match_workspace_group.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
