from yeeducli.utility.json_utils import response_validator, response_json_custom_order
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import LOOKUP_AUTH_RULES_ORDER
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class IamLookup:
    def list_resources():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/resources"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def describe_resource(resource_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/resource/{resource_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_permissions():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/permissions"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def describe_permission(permission_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/permission/{permission_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_roles():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/roles"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def describe_role(role_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/role/{role_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_rules():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/rules"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            if (response.status_code == 200 and isinstance(response.json(), list)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, LOOKUP_AUTH_RULES_ORDER)
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def describe_rule(rule_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/rule/{rule_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('error') is None)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, LOOKUP_AUTH_RULES_ORDER)
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_workspace_permissions():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/permissions"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get__workspace_permission(permission_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/permission/{permission_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
