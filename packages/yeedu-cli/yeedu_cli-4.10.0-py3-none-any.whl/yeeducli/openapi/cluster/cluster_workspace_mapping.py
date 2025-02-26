from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class ClusterWorkspaceMapping:
    def associate_workspace(workspace_id, cluster_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/cluster/{cluster_id}"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def dissociate_workspace(workspace_id, cluster_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/cluster/{cluster_id}"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_cluster_workspaces(cluster_id, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/cluster/{cluster_id}/workspaces"

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

    def search_cluster_workspaces(cluster_id, workspace_name, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/cluster/{cluster_id}/workspaces/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "workspace_name": workspace_name,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_workspace_clusters(workspace_id, pageNumber, limit, cluster_status=None, job_type=None, enable=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/clusters"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_status": cluster_status.split(",") if cluster_status is not None else cluster_status,
                    "job_type": job_type,
                    "pageNumber": pageNumber,
                    "limit": limit,
                    "enable": enable
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_workspace_clusters(workspace_id, cluster_name, pageNumber, limit, cluster_status=None, job_type=None, enable=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/ac/workspace/{workspace_id}/clusters/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_name": cluster_name,
                    "cluster_status": cluster_status.split(",") if cluster_status is not None else cluster_status,
                    "job_type": job_type,
                    "pageNumber": pageNumber,
                    "limit": limit,
                    "enable": enable
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
