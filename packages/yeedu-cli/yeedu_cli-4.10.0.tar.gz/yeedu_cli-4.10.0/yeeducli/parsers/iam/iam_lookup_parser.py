from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class IamLookupParser:

    def iam_lookup_parser(subparser):
        list_resources = subparser.add_parser(
            'list-resources',
            help='To get all the resources.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_resources.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_resources.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_resource = subparser.add_parser(
            'get-resource',
            help='To get resource details for a specific Resource.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_resource.add_argument(
            "--resource_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide the resource_id to get information about a specific Resource."
        )
        describe_resource.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_resource.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_permissions = subparser.add_parser(
            'list-permissions',
            help='To get all the Permission Types.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_permissions.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_permissions.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_permission = subparser.add_parser(
            'get-permission',
            help='To get resource details for a specific Permission Type.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_permission.add_argument(
            "--permission_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide the permission_id to get information about a specific Permission Type."
        )
        describe_permission.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_permission.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_roles = subparser.add_parser(
            'list-roles',
            help='To get all the Roles.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_roles.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_roles.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_role = subparser.add_parser(
            'get-role',
            help='To get resource details for a specific Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide the role_id to get information about a specific Role."
        )
        describe_role.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_role.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_rules = subparser.add_parser(
            'list-rules',
            help='To get all the Rules.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_rules.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_rules.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_rule = subparser.add_parser(
            'get-rule',
            help='To get resource details for a specific Rule.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_rule.add_argument(
            "--rule_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide the rule_id to get information about a specific Rule."
        )
        describe_rule.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_rule.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_workspace_permissions = subparser.add_parser(
            'list-workspace-permissions',
            help='To list all the Workspace Access Control Permissions.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_workspace_permissions.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_workspace_permissions.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_workspace_permission = subparser.add_parser(
            'get-workspace-permission',
            help='To get Workspace Access Control Permission details for a specific Permission Id.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_workspace_permission.add_argument(
            "--permission_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide the permission_id to get information about a specific Workspace Access Control Permission."
        )
        get_workspace_permission.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_workspace_permission.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
