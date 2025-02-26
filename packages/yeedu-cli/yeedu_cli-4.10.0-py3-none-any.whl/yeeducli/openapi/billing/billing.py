from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys
import json
import urllib.parse

logger = Logger.get_logger(__name__, True)


class Billing:

    def list_billed_tenants(billing_type):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/billing/tenants"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "billing": billing_type
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_billed_date_range(billing_type, tenant_ids=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/billing/date/range"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "billing": billing_type,
                    "tenant_ids": tenant_ids.split(",") if tenant_ids is not None else tenant_ids
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_billed_clusters(billing_type, tenant_ids=None, cloud_providers=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/billing/clusters"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "billing": billing_type,
                    "tenant_ids": tenant_ids.split(",") if tenant_ids is not None else tenant_ids,
                    "cloud_providers": cloud_providers
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_billed_machine_types(billing_type, tenant_ids=None, cloud_providers=None, cluster_ids=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/billing/machine_types"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "billing": billing_type,
                    "tenant_ids": tenant_ids.split(",") if tenant_ids is not None else tenant_ids,
                    "cloud_providers": cloud_providers,
                    "cluster_ids": cluster_ids
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_billed_labels(billing_type, tenant_ids=None, cloud_providers=None, cluster_ids=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/billing/labels"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "billing": billing_type,
                    "tenant_ids": tenant_ids.split(",") if tenant_ids is not None else tenant_ids,
                    "cloud_providers": cloud_providers,
                    "cluster_ids": cluster_ids
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_billed_usage(start_date, end_date, tenant_ids=None, cloud_providers=None, cluster_ids=None, machine_type_ids=None, labels=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/billing/usage"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "tenant_ids": tenant_ids.split(',') if tenant_ids is not None else None,
                    "start_date": start_date,
                    "end_date": end_date,
                    "cloud_providers": cloud_providers,
                    "cluster_ids": cluster_ids,
                    "machine_type_ids": machine_type_ids,
                    "labels": (json.dumps(labels)).replace(" ", "") if labels is not None else None
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_billed_invoice(start_month_year, end_month_year, tenant_ids=None, cloud_providers=None, cluster_ids=None, machine_type_ids=None, labels=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/billing/invoice"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "tenant_ids": tenant_ids.split(',') if tenant_ids is not None else None,
                    "start_month_year": start_month_year,
                    "end_month_year": end_month_year,
                    "cloud_providers": cloud_providers,
                    "cluster_ids": cluster_ids,
                    "machine_type_ids": machine_type_ids,
                    "labels": (json.dumps(labels)).replace(" ", "") if labels is not None else None
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
