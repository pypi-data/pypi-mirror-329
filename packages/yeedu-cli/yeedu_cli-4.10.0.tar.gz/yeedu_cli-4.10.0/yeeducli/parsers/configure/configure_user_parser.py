from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class ConfigureUserParser:

    def configure_user_parser(configure_user_parser):
        configure_user_parser.add_argument(
            "--timeout",
            type=check_non_empty_string,
            nargs='?',
            default="48",
            help="Provide token expiration timeout in hour Example: --timeout=24,--timeout=infinity (infinity for no expiration time) to generate Yeedu Token."
        )
        configure_user_parser.add_argument(
            "--no-browser",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="If 'no-browser=true' is provided, the browser will not open automatically for the SSO login URL."
        )
        configure_user_parser.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        configure_user_parser.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

    def user_logout_parser(user_logout_parser):
        user_logout_parser.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        user_logout_parser.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
