from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class ObjectStorageManager:
    def list_object_storage_manager(pageNumber, limit, cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_managers"

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

    def search_object_storage_manager(object_storage_manager_name, pageNumber, limit, cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_managers/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "object_storage_manager_name": object_storage_manager_name,
                    "cloud_provider": cloud_provider,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_object_storage_manager_by_id_or_name(object_storage_manager_id=None, object_storage_manager_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "object_storage_manager_id": object_storage_manager_id,
                    "object_storage_manager_name": object_storage_manager_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_object_storage_manager(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager"

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

    def edit_object_storage_manager_by_id_or_name(json_data, object_storage_manager_id=None, object_storage_manager_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                data=json_data,
                params={
                    "object_storage_manager_id": object_storage_manager_id,
                    "object_storage_manager_name": object_storage_manager_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_object_storage_manager_by_id_or_name(object_storage_manager_id=None, object_storage_manager_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "object_storage_manager_id": object_storage_manager_id,
                    "object_storage_manager_name": object_storage_manager_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
