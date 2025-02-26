from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class WorkspaceAccessControl:
    def list_workspace_users(workspace_id, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/users"

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

    def list_workspace_users_access(workspace_id, pageNumber, limit, permission_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/users/permission"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "permission_id": permission_id,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_workspace_users_access(workspace_id, username, pageNumber, limit, permission_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/users/permission/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "username": username,
                    "permission_id": permission_id,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_workspace_users(workspace_id, username, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/users/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "username": username,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def match_workspace_user(workspace_id, username):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/user/match/{username}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_workspace_groups(workspace_id, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/groups"

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

    def list_workspace_groups_access(workspace_id, pageNumber, limit, permission_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/groups/permission"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "permission_id": permission_id,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_workspace_groups_access(workspace_id, groupname, pageNumber, limit, permission_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/groups/permission/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "groupname": groupname,
                    "permission_id": permission_id,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_workspace_groups(workspace_id, groupname, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/groups/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "groupname": groupname,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def match_workspace_group(workspace_id, groupname):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/group/match/{groupname}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_workspace_user_access(workspace_id, user_id):
        try:

            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/user/{user_id}/permission"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_workspace_group_access(workspace_id, group_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/group/{group_id}/permission"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def create_workspace_user_access(workspace_id, json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/user"

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

    def create_workspace_group_access(workspace_id, json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/group"

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

    def delete_workspace_user_access(workspace_id, user_id, permission_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/user/{user_id}/permission/{permission_id}"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_workspace_group_access(workspace_id, group_id, permission_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/group/{group_id}/permission/{permission_id}"

            response = Requests(
                url,
                method="DELETE",
                headers=config.headers,
                timeout=60
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
