from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class NotebookInstance:

    def list_notebook_instances(workspace_id, page_number, limit, cluster_ids=None, notebook_conf_ids=None, notebook_status=None, job_type_langs=None, created_by_ids=None, modified_by_ids=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/notebooks"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_ids": cluster_ids,
                    "notebook_conf_ids": notebook_conf_ids,
                    "notebook_status": [status.upper() for status in notebook_status] if isinstance(notebook_status, list) else None,
                    "job_type_langs": job_type_langs,
                    "created_by_ids": created_by_ids,
                    "modified_by_ids": modified_by_ids,
                    "pageNumber": page_number,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_notebook_instance_by_workspaceId_and_name(workspace_id, notebook_name, page_number, limit, cluster_ids=None, notebook_conf_ids=None, notebook_status=None, job_type_langs=None, created_by_ids=None, modified_by_ids=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/notebooks/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "notebook_name": notebook_name,
                    "cluster_ids": cluster_ids,
                    "notebook_conf_ids": notebook_conf_ids,
                    "notebook_status":  [status.upper() for status in notebook_status] if isinstance(notebook_status, list) else None,
                    "job_type_langs": job_type_langs,
                    "created_by_ids": created_by_ids,
                    "modified_by_ids": modified_by_ids,
                    "pageNumber": page_number,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_notebook_instance(workspace_id, json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/notebook"

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

    def notebook_instance_kernel_start(workspace_id, notebook_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/notebook/{notebook_id}/kernel/startOrGetStatus"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def notebook_instance_kernel_status(workspace_id, notebook_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/notebook/{notebook_id}/kernel/status"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def notebook_instance_kernel_interrupt(workspace_id, notebook_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/notebook/{notebook_id}/kernel/interrupt"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def notebook_instance_kernel_restart(workspace_id, notebook_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/notebook/{notebook_id}/kernel/restart"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_notebook_inst_by_id(workspace_id, notebook_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/notebook/{notebook_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def stop_notebook_instance_by_id(workspace_id, notebook_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/notebook/kill/{notebook_id}"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
