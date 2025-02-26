from yeeducli.utility.logger_utils import Logger
from dotenv import load_dotenv
import os
import sys
import requests

load_dotenv()

logger = Logger.get_logger(__name__, True)


class Requests:

    def __init__(self, url, method, headers, timeout=60, json=None, data=None, files=None, stream=None, params=None):
        self.url = url
        self.method = method
        self.headers = headers
        self.timeout = timeout
        self.json = json
        self.data = data
        self.files = files
        self.stream = stream
        self.params = params

    def check_ssl(self):
        try:
            # if not provided set to true by default

            yeedu_cli_verify_ssl = os.getenv(
                'YEEDU_CLI_VERIFY_SSL', 'true').lower()

            if yeedu_cli_verify_ssl == 'true':

                # check for the ssl cert dir
                if not os.getenv('YEEDU_SSL_CERT_FILE'):
                    logger.error(
                        f"Please set the environment variable: YEEDU_SSL_CERT_FILE if YEEDU_CLI_VERIFY_SSL is set to: {yeedu_cli_verify_ssl} (default: true)")
                    sys.exit(-1)
                else:

                    # check if the file exists or not
                    if os.path.isfile(os.getenv('YEEDU_SSL_CERT_FILE')):
                        return os.getenv('YEEDU_SSL_CERT_FILE')
                    else:
                        logger.error(
                            f"Provided YEEDU_SSL_CERT_FILE: {os.getenv('YEEDU_SSL_CERT_FILE')} doesnot exists")
                        sys.exit(-1)
            elif yeedu_cli_verify_ssl == 'false':
                return False
            else:
                logger.error(
                    f"Provided YEEDU_CLI_VERIFY_SSL: {os.getenv('YEEDU_CLI_VERIFY_SSL')} is neither true/false")
                sys.exit(-1)
        except Exception as e:
            logger.error(f"Check SSL failed due to: {e}")
            sys.exit(-1)

    def send_http_request(self):
        try:
            response = requests.request(
                self.method,
                self.url,
                headers=self.headers,
                timeout=self.timeout,
                params=self.params,
                data=self.data,
                json=self.json,
                files=self.files,
                stream=self.stream,
                verify=self.check_ssl()
            )

            return response
        except Exception as e:
            logger.error(f"HTTP request failed due to: {e}")
            sys.exit(-1)
