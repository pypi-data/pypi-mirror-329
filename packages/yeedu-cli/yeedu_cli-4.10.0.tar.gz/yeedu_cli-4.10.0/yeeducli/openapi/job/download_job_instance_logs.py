from yeeducli.utility.file_utils import FileUtils
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class DownloadJobInstanceLogs:
    def get_job_instance_log_records(workspace_id, log_type, job_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job/{job_id}/log/{log_type}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                stream=True
            ).send_http_request()

            return FileUtils.process_file_response(response, save_to_disk=False)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
