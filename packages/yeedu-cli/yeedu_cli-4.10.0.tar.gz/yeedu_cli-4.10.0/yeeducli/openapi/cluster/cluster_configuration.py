from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class ClusterConfiguration:
    def list_cluster_config(pageNumber, limit, cloud_provider=None, compute_type=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/confs"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cloud_provider": cloud_provider,
                    "compute_type": compute_type,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_cluster_config(cluster_conf_name, pageNumber, limit, cloud_provider=None, compute_type=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/confs/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_conf_name": cluster_conf_name,
                    "cloud_provider": cloud_provider,
                    "compute_type": compute_type,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_cluster_config(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf"

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

    def get_cluster_config_by_id_or_name(cluster_conf_id=None, cluster_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cluster_conf_id": cluster_conf_id,
                    "cluster_conf_name": cluster_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_cluster_config(json_data, cluster_conf_id=None, cluster_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                data=json_data,
                params={
                    "cluster_conf_id": cluster_conf_id,
                    "cluster_conf_name": cluster_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_cluster_config_by_id_or_name(cluster_conf_id=None, cluster_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "cluster_conf_id": cluster_conf_id,
                    "cluster_conf_name": cluster_conf_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
