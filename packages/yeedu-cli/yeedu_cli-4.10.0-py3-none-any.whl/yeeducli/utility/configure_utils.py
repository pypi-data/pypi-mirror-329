from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import CONFIG_FILE_PATH, YEEDU_HIDDEN_DIR, CREDENTIALS_FILE_PATH
from dotenv import load_dotenv
from os.path import exists
import os
import sys
import json

load_dotenv()

logger = Logger.get_logger(__name__, True)


class ConfigFile:

    def __init__(self):
        pass

    def writeToConfig(token_json):
        try:
            if not os.getenv('YEEDU_RESTAPI_TOKEN_FILE_PATH'):
                os.makedirs(YEEDU_HIDDEN_DIR, mode=0o777, exist_ok=True)

            if not os.path.isfile(CONFIG_FILE_PATH):
                with open(f"{CONFIG_FILE_PATH}", "w") as configfile:
                    json.dump(token_json, configfile)
                    configfile.close()
            else:
                with open(f"{CONFIG_FILE_PATH}", "r") as configfile:
                    new_token = json.load(configfile)
                    configfile.close()

                new_token["token"] = json.loads(
                    json.dumps(token_json))["token"]
                with open(f"{CONFIG_FILE_PATH}", "w") as configfile:
                    json.dump(new_token, configfile)
                    configfile.close()
        except Exception as e:
            logger.error(f"Failed due to: {e}")
            sys.exit(-1)

    def findKeyInFile(self, credentials, key):
        if key in credentials.keys():
            if credentials.get(key):
                return credentials[key]
            else:
                logger.error(
                    f"The value for {key} key does not exists in the file: {CREDENTIALS_FILE_PATH}")
                sys.exit(-1)
        else:
            logger.error(
                f"The key {key} does not exists in the file: {CREDENTIALS_FILE_PATH} ")
            sys.exit(-1)

    def checkAndConfigureUserAndPass(self):
        # check for env variables as priority
        try:
            if (os.getenv("YEEDU_USERNAME") and os.getenv("YEEDU_PASSWORD")) is not None:
                return os.getenv("YEEDU_USERNAME"), os.getenv("YEEDU_PASSWORD")
            elif exists(CREDENTIALS_FILE_PATH):
                try:
                    with open(f"{CREDENTIALS_FILE_PATH}", "r") as credentialsFile:
                        credentials = json.load(credentialsFile)
                        credentialsFile.close()

                    # checking if the key and it's value exists or not and returning it
                    return self.findKeyInFile(credentials, "YEEDU_USERNAME"),  self.findKeyInFile(credentials, "YEEDU_PASSWORD")
                except Exception as e:
                    logger.error(
                        f"Error: Check the JSON inside yeedu_credentials.config at path: {CREDENTIALS_FILE_PATH},\n{e}")
                    sys.exit(-1)
            else:
                return '', ''
                # else:
                #     json_example = {
                #         "YEEDU_USERNAME": "USER",
                #         "YEEDU_PASSWORD": "PASS"
                #     }
                #     logger.error(
                #         f"Please set the environment variables: \n YEEDU_USERNAME and YEEDU_PASSWORD \nor\nStore the credentials in yeedu_credentials.config at path: {YEEDU_HIDDEN_DIR} as \n{json_example}")
                #     sys.exit(-1)
        except Exception as e:
            logger.error(f"Failed due to: {e}")
