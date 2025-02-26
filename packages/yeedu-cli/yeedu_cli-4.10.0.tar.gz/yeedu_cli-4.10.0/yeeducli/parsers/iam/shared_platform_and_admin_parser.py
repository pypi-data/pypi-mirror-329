from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class SharedPlatformAndAdminParser:

    def shared_platform_and_admin_parser(subparser):

        sync_user = subparser.add_parser(
            'sync-user',
            help='To get the information about a specific User.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        sync_user.add_argument(
            "--username",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide username to get information about a specific User."
        )
        sync_user.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        sync_user.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        sync_group = subparser.add_parser(
            'sync-group',
            help='To get the information about a specific Group.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        sync_group.add_argument(
            "--groupname",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide groupname to get information about a specific Group."
        )
        sync_group.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        sync_group.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_user_groups = subparser.add_parser(
            'list-user-groups',
            help='To list all the groups for a specific User.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_user_groups.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide user_id to list all the groups for a specific User."
        )
        list_user_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups for a specific page_number."
        )
        list_user_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups."
        )
        list_user_groups.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_user_groups.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_users = subparser.add_parser(
            'list-users',
            help='To list all the available Users.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_users.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide group_id to list all the users for a specific group."
        )
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

        list_group_users = subparser.add_parser(
            'list-group-users',
            help='To list all the users for a specific group.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_group_users.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide group_id to list all the users for a specific Group."
        )
        list_group_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users for a specific page_number."
        )
        list_group_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users."
        )
        list_group_users.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_group_users.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_groups = subparser.add_parser(
            'list-groups',
            help='To list all the available Groups.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_groups.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide user_id to list all the groups of a specific user."
        )
        list_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users for a specific page_number."
        )
        list_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users."
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

        search_users = subparser.add_parser(
            'search-users',
            help='To search the users based on username.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_users.add_argument(
            "--username",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide username to search users matching username."
        )
        search_users.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide group_id to search all the users of a specific group."
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

        match_user = subparser.add_parser(
            'match-user',
            help='To get the users based on matching username.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        match_user.add_argument(
            "--username",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide username to get user details."
        )
        match_user.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        match_user.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_groups = subparser.add_parser(
            'search-groups',
            help='To search the groups based on groupname.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_groups.add_argument(
            "--groupname",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To search all the groups matching provided groupname."
        )
        search_groups.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide user_id to search all the groups of a specific user."
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

        match_group = subparser.add_parser(
            'match-group',
            help='To get the groups based on matching groupname.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        match_group.add_argument(
            "--groupname",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide groupname to get information about matching groups."
        )
        match_group.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        match_group.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
