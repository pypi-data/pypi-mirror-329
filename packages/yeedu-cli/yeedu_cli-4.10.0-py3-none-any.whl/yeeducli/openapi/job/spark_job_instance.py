from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class SparkJobInstance:

    def list_spark_job_instances(workspace_id, page_number, limit, cluster_ids=None, job_conf_ids=None, job_status=None, job_type=None, job_type_langs=None, created_by_ids=None, modified_by_ids=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/jobs"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_ids": cluster_ids,
                    "job_conf_ids": job_conf_ids,
                    "job_status": [status.upper() for status in job_status] if isinstance(job_status, list) else None,
                    "job_type": job_type,
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

    def search_spark_job_instance_by_workspaceId_and_name(workspace_id, job_conf_name, pageNumber, limit, cluster_ids=None, job_status=None, job_type=None, job_type_langs=None, created_by_ids=None, modified_by_ids=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/jobs/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "job_conf_name": job_conf_name,
                    "cluster_ids": cluster_ids,
                    "job_status": [status.upper() for status in job_status] if isinstance(job_status, list) else None,
                    "job_type": job_type,
                    "job_type_langs": job_type_langs,
                    "created_by_ids": created_by_ids,
                    "modified_by_ids": modified_by_ids,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_spark_job_instance(workspace_id, json_data):
        try:
           
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job"

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

    def get_spark_job_inst_by_id(workspace_id, job_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job/{job_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def stop_spark_job_instance_by_id(workspace_id, job_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job/kill/{job_id}"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_workflow_job_instance_details_by_appId(workspace_id, job_application_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job/workflow_job_instance_details/{job_application_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_spark_job_status_by_id(workspace_id, job_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job/{job_id}/status"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
