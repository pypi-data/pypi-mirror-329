from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class CredentialsConfig:
    def list_credentials_config(pageNumber, limit, cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/credential_configs"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cloud_provider": cloud_provider,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_credentials_config(credentials_conf_name, pageNumber, limit, cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/credential_configs/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "credentials_conf_name": credentials_conf_name,
                    "cloud_provider": cloud_provider,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_credentials_config(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/credential_config"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_credentials_config_by_id_or_name(credentials_conf_id=None, credentials_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/credential_config"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "credentials_conf_id": credentials_conf_id,
                    "credentials_conf_name": credentials_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_credentials_config_by_id_or_name(json_data, credentials_conf_id=None, credentials_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/credential_config"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                data=json_data,
                params={
                    "credentials_conf_id": credentials_conf_id,
                    "credentials_conf_name": credentials_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_credentials_config_by_id_or_name(credentials_conf_id=None, credentials_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/credential_config"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "credentials_conf_id": credentials_conf_id,
                    "credentials_conf_name": credentials_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
