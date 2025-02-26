from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class User:
    def list_tenants(pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/tenants"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_tenants(tenant_name, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/tenants/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "tenant_name": tenant_name,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def associate_tenant(tenant_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/select/{tenant_id}"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_user_info():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/info"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_user_roles(tenant_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/info/roles"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    'tenant_id': tenant_id
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)
