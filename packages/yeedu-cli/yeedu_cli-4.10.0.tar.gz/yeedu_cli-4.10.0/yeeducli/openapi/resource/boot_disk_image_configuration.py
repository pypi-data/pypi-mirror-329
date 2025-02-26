from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class BootDiskImageConfiguration:

    def add_boot_disk_image_config(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/boot_disk_image"

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

    def list_boot_disk_image_config(page_number, limit, cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/boot_disk_images"

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

    def search_boot_disk_image_config(boot_disk_image_name, page_number, limit, cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/boot_disk_images/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "boot_disk_image_name": boot_disk_image_name,
                    "cloud_provider": cloud_provider,
                    "pageNumber": page_number,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_boot_disk_image_config(boot_disk_image_id=None, boot_disk_image_name=None):
        try:
            url = f'{config.YEEDU_RESTAPI_URL}/machine/boot_disk_image'

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "boot_disk_image_id": boot_disk_image_id,
                    "boot_disk_image_name": boot_disk_image_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_boot_disk_image_config(json_data, boot_disk_image_id=None, boot_disk_image_name=None):
        try:
            url = f'{config.YEEDU_RESTAPI_URL}/machine/boot_disk_image'

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                data=json_data,
                params={
                    "boot_disk_image_id": boot_disk_image_id,
                    "boot_disk_image_name": boot_disk_image_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_boot_disk_image_config(boot_disk_image_id=None, boot_disk_image_name=None):
        try:
            url = f'{config.YEEDU_RESTAPI_URL}/machine/boot_disk_image'

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "boot_disk_image_id": boot_disk_image_id,
                    "boot_disk_image_name": boot_disk_image_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
