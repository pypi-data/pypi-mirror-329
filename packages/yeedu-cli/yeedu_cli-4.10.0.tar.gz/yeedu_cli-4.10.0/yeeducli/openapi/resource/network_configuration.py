from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class NetworkConfiguration:
    def list_network_config_by_cp_id(page_number, limit, cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/networks"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cloud_provider": cloud_provider,
                    "pageNumber": page_number,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_network_config_by_cp_id(network_conf_name, page_number, limit, cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/networks/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "network_conf_name": network_conf_name,
                    "cloud_provider": cloud_provider,
                    "pageNumber": page_number,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_network_config_by_cp_id(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/network"

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

    def get_network_config_by_id_or_name(network_conf_id=None, network_conf_name=None):
        try:

            url = f"{config.YEEDU_RESTAPI_URL}/machine/network"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "network_conf_id": network_conf_id,
                    "network_conf_name": network_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_network_config_by_id_or_name(json_data, network_conf_id=None, network_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/network"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                data=json_data,
                params={
                    "network_conf_id": network_conf_id,
                    "network_conf_name": network_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_network_config_by_id_or_name(network_conf_id=None, network_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/network"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "network_conf_id": network_conf_id,
                    "network_conf_name": network_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
