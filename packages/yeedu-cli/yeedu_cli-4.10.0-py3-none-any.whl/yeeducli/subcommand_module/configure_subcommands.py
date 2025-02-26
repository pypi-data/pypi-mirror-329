from yeeducli.openapi.configure.configure_user import ConfigureUser
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.configure_utils import ConfigFile
from yeeducli.utility.json_utils import *


logger = Logger.get_logger(__name__, True)


def configure_user(args):
    try:
        json_data = trim_namespace_json(args)

        configFile = ConfigFile()

        username, password = configFile.checkAndConfigureUserAndPass()

        response_json = ConfigureUser.generate_token(
            username,
            password,
            json_data.get("no_browser"),
            json_data.get('timeout')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def user_logout(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = ConfigureUser.logout()

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
