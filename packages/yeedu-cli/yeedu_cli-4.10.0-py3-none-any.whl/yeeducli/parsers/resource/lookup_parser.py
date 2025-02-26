from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string
from yeeducli.constants import CLOUD_PROVIDERS_LIST


class LookupParser:

    def lookup_parser(subparser):

        list_cloud_pov = subparser.add_parser(
            'list-providers',
            help='To get information about all Cloud Providers.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_cloud_pov.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_cloud_pov.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_cloud_prov = subparser.add_parser(
            'get-provider',
            help='To get information about a specific Cloud Provider.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_cloud_prov.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide specific cloud provider id to get-provider."
        )
        describe_cloud_prov.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_cloud_prov.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_cloud_prov_az = subparser.add_parser(
            'list-provider-availability-zones',
            help='To get information about Availability Zones for a specific Cloud Provider.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_cloud_prov_az.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide specific Cloud Provider id to list-provider-availability-zones."
        )
        list_cloud_prov_az.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of availability zones."
        )
        list_cloud_prov_az.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list availability zones for a specific page_number."
        )
        list_cloud_prov_az.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_cloud_prov_az.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_cloud_prov_az = subparser.add_parser(
            'get-provider-availability-zone',
            help='To get information about a specific Availability Zone for a specific Cloud Provider.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_cloud_prov_az.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide specific cloud provider id to get-provider-availability-zone."
        )
        describe_cloud_prov_az.add_argument(
            "--availability_zone_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide specific Availability Zone id to get-provider-availability-zone."
        )
        describe_cloud_prov_az.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_cloud_prov_az.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_cloud_prov_mt = subparser.add_parser(
            'list-provider-machine-types',
            help='To get information about Machine Types for a specific Cloud Provider.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_cloud_prov_mt.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide specific cloud provider id to list-provider-machine-types."
        )
        list_cloud_prov_mt.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of machine types."
        )
        list_cloud_prov_mt.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list machine types for a specific page_number."
        )
        list_cloud_prov_mt.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_cloud_prov_mt.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_cloud_prov_mt = subparser.add_parser(
            'get-provider-machine-type',
            help='To get information about a specific Machine Type for a specific Cloud Provider.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_cloud_prov_mt.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide specific cloud provider id to get-provider-machine-type."
        )
        describe_cloud_prov_mt.add_argument(
            "--machine_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide specific machine type id to get-provider-machine-type."
        )
        describe_cloud_prov_mt.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_cloud_prov_mt.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_disk_machine_type = subparser.add_parser(
            'list-disk-machine-types',
            help='To get information about all disk machine types.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_disk_machine_type.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_disk_machine_type.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_credential_type = subparser.add_parser(
            'list-credential-types',
            help='To get information about all credential types.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_credential_type.add_argument(
            "--cloud_provider",
            type=check_non_empty_string,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide specific cloud_provider to get information about related  credential types."
        )
        list_credential_type.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_credential_type.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_lookup_engine_cluster_instance_status = subparser.add_parser(
            'list-engine-cluster-instance-status',
            help='To get information about all available engine cluster instance status.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_lookup_engine_cluster_instance_status.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_lookup_engine_cluster_instance_status.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_lookup_spark_compute_type = subparser.add_parser(
            'list-spark-compute-types',
            help='To get information about all spark compute types.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_lookup_spark_compute_type.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_lookup_spark_compute_type.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_lookup_spark_infra_version = subparser.add_parser(
            'list-spark-infra-versions',
            help='To get information about spark infra version.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_lookup_spark_infra_version.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_lookup_spark_infra_version.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_lookup_spark_job_status = subparser.add_parser(
            'list-spark-job-status',
            help='To get information about spark job status.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_lookup_spark_job_status.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_lookup_spark_job_status.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_lookup_workflow_execution_state = subparser.add_parser(
            'list-workflow-execution-states',
            help='To get information about workflow execution state.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_lookup_workflow_execution_state.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_lookup_workflow_execution_state.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_lookup_workflow_type = subparser.add_parser(
            'list-workflow-types',
            help='To get information about workflow type.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_lookup_workflow_type.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_lookup_workflow_type.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_linux_distros = subparser.add_parser(
            'list-linux-distros',
            help='To get information about all the linux distributions.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_linux_distros.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_linux_distros.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
