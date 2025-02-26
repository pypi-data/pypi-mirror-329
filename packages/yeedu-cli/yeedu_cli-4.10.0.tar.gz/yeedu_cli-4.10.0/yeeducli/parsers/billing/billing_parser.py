from yeeducli.constants import CLOUD_PROVIDERS_LIST
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_array_of_intgers, check_choices
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from datetime import date


class BillingParser:

    def billing_parser(subparser):

        list_billed_tenants = subparser.add_parser(
            'tenants',
            help='To retrieve a list of billed tenants.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_billed_tenants.add_argument(
            "--billing_type",
            type=check_non_empty_string,
            nargs='?',
            choices=['usage', 'invoice'],
            default='usage',
            help="Specifies the billing type to be used as a filter."
        )
        list_billed_tenants.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_billed_tenants.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_billed_date_range = subparser.add_parser(
            'date-range',
            help='To retrieve a list of billed date range.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_billed_date_range.add_argument(
            "--billing_type",
            type=check_non_empty_string,
            nargs='?',
            choices=['usage', 'invoice'],
            default='usage',
            help="Specifies the billing type to be used as a filter."
        )
        list_billed_date_range.add_argument(
            "--tenant_ids",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Specifies the tenant IDs to be used as a filter."
        )
        list_billed_date_range.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_billed_date_range.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_billed_clusters = subparser.add_parser(
            'clusters',
            help='To retrieve a list of billed clusters.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_billed_clusters.add_argument(
            "--billing_type",
            type=check_non_empty_string,
            nargs='?',
            choices=['usage', 'invoice'],
            default='usage',
            help="Specifies the billing type to be used as a filter."
        )
        list_billed_clusters.add_argument(
            "--tenant_ids",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Specifies the tenant IDs to be used as a filter."
        )
        list_billed_clusters.add_argument(
            "--cloud_providers",
            type=lambda values: check_choices(
                values, choices=CLOUD_PROVIDERS_LIST),
            nargs='?',
            default=SUPPRESS,
            help="Specifies the cloud providers to be used as a filter. Choices are: " +
            ", ".join(CLOUD_PROVIDERS_LIST)
        )
        list_billed_clusters.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_billed_clusters.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_billed_machine_types = subparser.add_parser(
            'machine-types',
            help='To retrieve a list of billed machine types.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_billed_machine_types.add_argument(
            "--billing_type",
            type=check_non_empty_string,
            nargs='?',
            choices=['usage', 'invoice'],
            default='usage',
            help="Specifies the billing type to be used as a filter."
        )
        list_billed_machine_types.add_argument(
            "--tenant_ids",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Specifies the tenant IDs to be used as a filter."
        )
        list_billed_machine_types.add_argument(
            "--cloud_providers",
            type=lambda values: check_choices(
                values, choices=CLOUD_PROVIDERS_LIST),
            nargs='?',
            default=SUPPRESS,
            help="Specifies the cloud providers to be used as a filter. Choices are: " +
            ", ".join(CLOUD_PROVIDERS_LIST)
        )
        list_billed_machine_types.add_argument(
            "--cluster_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="Specifies the cluster instance IDs to be used as a filter."
        )
        list_billed_machine_types.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_billed_machine_types.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_billed_labels = subparser.add_parser(
            'labels',
            help='To retrieve a list of billed cluster labels.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_billed_labels.add_argument(
            "--billing_type",
            type=check_non_empty_string,
            nargs='?',
            choices=['usage', 'invoice'],
            default='usage',
            help="Specifies the billing type to be used as a filter."
        )
        list_billed_labels.add_argument(
            "--tenant_ids",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Specifies the tenant IDs to be used as a filter."
        )
        list_billed_labels.add_argument(
            "--cloud_providers",
            type=lambda values: check_choices(
                values, choices=CLOUD_PROVIDERS_LIST),
            nargs='?',
            default=SUPPRESS,
            help="Specifies the cloud providers to be used as a filter. Choices are: " +
            ", ".join(CLOUD_PROVIDERS_LIST)
        )
        list_billed_labels.add_argument(
            "--cluster_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="Specifies the cluster instance IDs to be used as a filter."
        )
        list_billed_labels.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_billed_labels.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_billed_usage = subparser.add_parser(
            'usage',
            help='To list the billed usage.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_billed_usage.add_argument(
            "--tenant_ids",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide the tenant_ids to list billed usage."
        )
        list_billed_usage.add_argument(
            "--start_date",
            nargs=1,
            type=date.fromisoformat,
            required=True,
            default=SUPPRESS,
            help="Provide the start_date of billed date."
        )
        list_billed_usage.add_argument(
            "--end_date",
            nargs=1,
            type=date.fromisoformat,
            required=True,
            default=SUPPRESS,
            help="Provide the end_date of billed date."
        )
        list_billed_usage.add_argument(
            "--cloud_providers",
            type=lambda values: check_choices(
                values, choices=CLOUD_PROVIDERS_LIST),
            nargs='?',
            default=SUPPRESS,
            help="Provide cloud_providers to list billed usage for given cloud providers. Choices are: " +
            ", ".join(CLOUD_PROVIDERS_LIST)
        )
        list_billed_usage.add_argument(
            "--cluster_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="Provide the cluster_ids to list billed usage."
        )
        list_billed_usage.add_argument(
            "--machine_type_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="Provide the machine_type_ids to list billed usage."
        )
        list_billed_usage.add_argument(
            "--labels",
            type=check_non_empty_string,
            action='append',
            default=SUPPRESS,
            nargs='+',
            help="Provide the labels key-value pair to list billed usage."
        )
        list_billed_usage.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_billed_usage.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_billed_invoice = subparser.add_parser(
            'invoice',
            help='To list the billed invoice.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_billed_invoice.add_argument(
            "--tenant_ids",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide the tenant_ids."
        )
        list_billed_invoice.add_argument(
            "--start_month_year",
            nargs=1,
            type=date.fromisoformat,
            required=True,
            default=SUPPRESS,
            help="Provide the start_month_year of billed date."
        )
        list_billed_invoice.add_argument(
            "--end_month_year",
            nargs=1,
            type=date.fromisoformat,
            required=True,
            default=SUPPRESS,
            help="Provide the end_month_year of billed date."
        )
        list_billed_invoice.add_argument(
            "--cloud_providers",
            type=lambda values: check_choices(
                values, choices=CLOUD_PROVIDERS_LIST),
            nargs='?',
            default=SUPPRESS,
            help="Provide cloud_providers to list billed invoice for given cloud providers. Choices are: " +
            ", ".join(CLOUD_PROVIDERS_LIST)
        )
        list_billed_invoice.add_argument(
            "--cluster_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="Provide the cluster_ids to list billed invoice."
        )
        list_billed_invoice.add_argument(
            "--machine_type_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="Provide the machine_type_ids list billed invoice."
        )
        list_billed_invoice.add_argument(
            "--labels",
            type=check_non_empty_string,
            action='append',
            default=SUPPRESS,
            nargs='+',
            help="Provide the labels as key-value pair list billed invoice."
        )
        list_billed_invoice.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_billed_invoice.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
