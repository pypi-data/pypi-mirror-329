from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class VolumeConfiguration:
    def list_volume_config(page_number, limit, cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/volumes"

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

    def search_volume_config(volume_conf_name, page_number, limit, cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/volumes/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "volume_conf_name": volume_conf_name,
                    "cloud_provider": cloud_provider,
                    "pageNumber": page_number,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_volume_config(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/volume"

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

    def get_volume_config_by_id_or_name(volume_conf_id=None, volume_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/volume"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "volume_conf_id": volume_conf_id,
                    "volume_conf_name": volume_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_volume_config_by_id_or_name(json_data, volume_conf_id=None, volume_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/volume"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                data=json_data,
                params={
                    "volume_conf_id": volume_conf_id,
                    "volume_conf_name": volume_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_volume_config_by_id_or_name(volume_conf_id=None, volume_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/volume"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "volume_conf_id": volume_conf_id,
                    "volume_conf_name": volume_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
