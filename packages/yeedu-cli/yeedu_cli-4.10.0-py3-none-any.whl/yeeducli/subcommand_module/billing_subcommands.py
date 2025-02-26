from yeeducli.openapi.billing.billing import Billing
from yeeducli.utility.json_utils import *
from yeeducli.utility.logger_utils import Logger
import sys

logger = Logger.get_logger(__name__, True)


# Billed Tenants
def list_billed_tenants(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = Billing.list_billed_tenants(
            json_data.get('billing_type')
        )

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Billed Date Range
def list_billed_date_range(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = Billing.list_billed_date_range(
            json_data.get('billing_type'),
            json_data.get('tenant_ids')
        )

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Billed Clusters
def list_billed_clusters(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = Billing.list_billed_clusters(
            json_data.get('billing_type'),
            json_data.get('tenant_ids'),
            json_data.get('cloud_providers')
        )

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Billed Machine Types
def list_billed_machine_types(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = Billing.list_billed_machine_types(
            json_data.get('billing_type'),
            json_data.get('tenant_ids'),
            json_data.get('cloud_providers'),
            json_data.get('cluster_ids')
        )

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Billed Labels
def list_billed_labels(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = Billing.list_billed_labels(
            json_data.get('billing_type'),
            json_data.get('tenant_ids'),
            json_data.get('cloud_providers'),
            json_data.get('cluster_ids')
        )

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Billed Usage
def list_billed_usage(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args, subcommand='usage'))

        response_json = Billing.list_billed_usage(
            json_data.get('start_date'), json_data.get('end_date'), json_data.get('tenant_ids'), json_data.get('cloud_providers'), json_data.get('cluster_ids'), json_data.get('machine_type_ids'), json_data.get('labels'))

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Billed Invoice
def list_billed_invoice(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args, subcommand='invoice'))

        response_json = Billing.list_billed_invoice(
            json_data.get('start_month_year'), json_data.get('end_month_year'), json_data.get('tenant_ids'), json_data.get('cloud_providers'), json_data.get('cluster_ids'), json_data.get('machine_type_ids'), json_data.get('labels'))

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
