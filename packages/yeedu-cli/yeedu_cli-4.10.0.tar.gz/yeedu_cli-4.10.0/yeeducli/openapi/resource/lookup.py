from yeeducli.utility.json_utils import response_validator, response_json_custom_order
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import CLOUD_PROVIDER_AVAILABILITY_ZONE_ORDER, CLOUD_PROVIDER_DISK_MACHINE_TYPE_ORDER, LOOKUP_CREDENTIAL_TYPES_ORDER
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class Lookup:

    def get_providers():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_cloud_providers"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_provider_by_id(cloud_provider_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_cloud_providers/{cloud_provider_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_az_by_provider_id(cloud_provider_id, limit, pageNumber):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_cloud_providers/{cloud_provider_id}/machine/available/zones"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            if (response.status_code == 200 and isinstance(response.json(), list)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, CLOUD_PROVIDER_AVAILABILITY_ZONE_ORDER)
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_az_by_provider_id_and_zone_id(cloud_provider_id, availablility_zone_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_cloud_providers/{cloud_provider_id}/machine/available/zones/{availablility_zone_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('error') is None)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, CLOUD_PROVIDER_AVAILABILITY_ZONE_ORDER)
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_machine_type_by_provider_id(cloud_provider_id, limit, pageNumber):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_cloud_providers/{cloud_provider_id}/machine/types"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_machine_type_by_provider_id_and_machine_type_id(cloud_provider_id, machine_type_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_cloud_providers/{cloud_provider_id}/machine/types/{machine_type_id}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_disk_machine_type():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_disk_machine_type"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            if (response.status_code == 200 and isinstance(response.json(), list)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, CLOUD_PROVIDER_DISK_MACHINE_TYPE_ORDER)
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_credential_type(cloud_provider=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_credential_type"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "cloud_provider": cloud_provider
                }
            ).send_http_request()

            if (response.status_code == 200 and isinstance(response.json(), list)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, LOOKUP_CREDENTIAL_TYPES_ORDER)
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_lookup_engine_cluster_instance_status():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_engine_cluster_instance_status"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_lookup_spark_compute_type():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_spark_compute_type"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_lookup_spark_infra_version():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_spark_infra_version"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_lookup_spark_job_status():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_spark_job_status"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_lookup_workflow_execution_state():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_workflow_execution_state"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_lookup_workflow_type():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_workflow_type"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_lookup_linux_distros():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/lookup_linux_distro"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
