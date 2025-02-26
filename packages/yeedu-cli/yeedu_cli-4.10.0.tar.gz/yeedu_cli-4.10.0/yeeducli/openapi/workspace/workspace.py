from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class Workspace:
    def list_workspaces(enable, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspaces"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "enable": enable,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def create_workspace(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace"

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

    def get_workspace_by_id_or_name(workspace_id=None, workspace_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_workspace_stats(workspace_id=None, workspace_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/stats"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_workspace_by_name(workspace_name, enable, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspaces/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "workspace_name": workspace_name,
                    "enable": enable,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_workspace_by_id_or_name(json_data, workspace_id=None, workspace_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                data=json_data,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def enable_workspace_by_id_or_name(workspace_id=None, workspace_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/enable"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def disable_workspace_by_id_or_name(workspace_id=None, workspace_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/disable"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def export_workspace(enable, workspace_id=None, workspace_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/export"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name,
                    "enable": enable
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def import_workspace(workspaceImport, permissive, overwrite, workspace_id=None, workspace_name=None, cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/import"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name,
                    "cluster_id": cluster_id,
                    "cluster_name": cluster_name,
                    "overwrite": overwrite,
                    "permissive": permissive
                },
                json=workspaceImport
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
