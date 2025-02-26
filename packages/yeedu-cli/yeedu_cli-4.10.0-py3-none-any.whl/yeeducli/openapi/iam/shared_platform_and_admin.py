from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class SharedPlatformAndAdmin:
    def sync_user(username):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/sync/user/{username}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def sync_group(groupname):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/sync/group/{groupname}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_users(pageNumber, limit, group_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/users"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "group_id": group_id,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_groups(pageNumber, limit, user_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/groups"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "user_id": user_id,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_users(username, pageNumber, limit, group_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/search/users"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "username": username,
                    "group_id": group_id,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_groups(groupname, pageNumber, limit, user_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/search/groups"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "groupname": groupname,
                    "user_id": user_id,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def match_user(username):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/match/user/{username}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def match_group(groupname):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/match/group/{groupname}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
