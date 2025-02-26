from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class PlatformAdmin:
    def list_tenants(pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenants"

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
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_tenant(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant"

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

    def get_tenant_by_id_or_name(tenant_id=None, tenant_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "tenant_id": tenant_id,
                    "tenant_name": tenant_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_tenant_by_id_or_name(tenant_id=None, tenant_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "tenant_id": tenant_id,
                    "tenant_name": tenant_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_tenant_by_id_or_name(json_data, tenant_id=None, tenant_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                data=json_data,
                params={
                    "tenant_id": tenant_id,
                    "tenant_name": tenant_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_user_tenants(user_id, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/user/{user_id}/tenants"

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
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_tenants(tenant_name, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenants/search"

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
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
