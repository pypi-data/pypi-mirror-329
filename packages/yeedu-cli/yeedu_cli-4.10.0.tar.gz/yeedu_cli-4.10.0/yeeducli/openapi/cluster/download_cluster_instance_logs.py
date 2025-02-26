from yeeducli.utility.file_utils import FileUtils
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class DownloadClusterInstanceLogs:
    def get_cluster_instance_log_records(log_type, cluster_id=None, cluster_name=None, cluster_status_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/log/{log_type}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                stream=True,
                params={
                    "cluster_id": cluster_id,
                    "cluster_name": cluster_name,
                    "cluster_status_id": cluster_status_id
                }
            ).send_http_request()

            return FileUtils.process_file_response(response, save_to_disk=False)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
