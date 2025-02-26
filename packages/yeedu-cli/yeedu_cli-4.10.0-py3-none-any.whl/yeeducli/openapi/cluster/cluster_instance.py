from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class ClusterInstance:
    def list_cluster_instance(pageNumber, limit, enable, cluster_conf_id=None, cluster_conf_name=None, cluster_status=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/clusters"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_conf_id": cluster_conf_id,
                    "cluster_conf_name": cluster_conf_name,
                    "cluster_status": cluster_status.split(',') if cluster_status is not None else None,
                    "pageNumber": pageNumber,
                    "limit": limit,
                    "enable": enable
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_cluster_instance(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster"

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

    def search_cluster_instance_by_name(cluster_name, pageNumber, limit, enable, cluster_conf_id=None, cluster_conf_name=None, cluster_status=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/clusters/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_name": cluster_name,
                    "cluster_conf_id": cluster_conf_id,
                    "cluster_conf_name": cluster_conf_name,
                    "cluster_status": cluster_status.split(',') if cluster_status is not None else None,
                    "enable": enable,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_id": cluster_id,
                    "cluster_name": cluster_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_cluster_instance(json_data, cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                data=json_data,
                params={
                    "cluster_id": cluster_id,
                    "cluster_name": cluster_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def destroy_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/destroy"

            request_body = {
                "cluster_id": cluster_id,
                "cluster_name": cluster_name
            }

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json={key: value for key, value in request_body.items()
                      if value is not None}
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def enable_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/enable"

            request_body = {
                "cluster_id": cluster_id,
                "cluster_name": cluster_name
            }

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                json={key: value for key, value in request_body.items()
                      if value is not None}
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def disable_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/disable"

            request_body = {
                "cluster_id": cluster_id,
                "cluster_name": cluster_name
            }

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                json={key: value for key, value in request_body.items()
                      if value is not None}
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def start_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/start"

            request_body = {
                "cluster_id": cluster_id,
                "cluster_name": cluster_name
            }

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json={key: value for key, value in request_body.items()
                      if value is not None}
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def stop_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/stop"

            request_body = {
                "cluster_id": cluster_id,
                "cluster_name": cluster_name
            }

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json={key: value for key, value in request_body.items()
                      if value is not None}
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_job_stats_by_cluster_instance_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/stats"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_id": cluster_id,
                    "cluster_name": cluster_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_cluster_status_by_cluster_instance_id_or_name(pageNumber, limit, cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/status"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_id": cluster_id,
                    "cluster_name": cluster_name,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def stop_all_jobs_on_cluster_instance(cluster_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/{cluster_id}/stop_all_jobs"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_cluster_errors_by_cluster_instance_id(cluster_id, cluster_status_id, pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/{cluster_id}/errors"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_status_id": cluster_status_id,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
