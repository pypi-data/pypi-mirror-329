from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class HiveMetastoreConfiguration:

    def add_hive_metastore_configuration(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_config"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_hive_metastore_config(page_number, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_configs"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "pageNumber": page_number,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_hive_metastore_config(hive_metastore_conf_name, page_number, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_configs/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "hive_metastore_conf_name": hive_metastore_conf_name,
                    "pageNumber": page_number,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_hive_metastore_config_by_id_or_name(hive_metastore_conf_id=None, hive_metastore_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_config"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "hive_metastore_conf_name": hive_metastore_conf_name,
                    "hive_metastore_conf_id": hive_metastore_conf_id
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_hive_metastore_config(json_data, hive_metastore_conf_id=None, hive_metastore_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_config"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                data=json_data,
                params={
                    "hive_metastore_conf_name": hive_metastore_conf_name,
                    "hive_metastore_conf_id": hive_metastore_conf_id
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_hive_metastore_config_by_id(hive_metastore_conf_id=None, hive_metastore_conf_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_config"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "hive_metastore_conf_name": hive_metastore_conf_name,
                    "hive_metastore_conf_id": hive_metastore_conf_id
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)
