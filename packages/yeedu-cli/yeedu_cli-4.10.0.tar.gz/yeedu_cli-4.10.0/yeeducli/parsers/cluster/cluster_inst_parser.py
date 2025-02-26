from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null, validate_integer_and_null
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.constants import CLUSTER_TYPE_LIST


class ClusterInstanceParser:

    def cluster_instance_parser(subparser):
        create_cluster_inst = subparser.add_parser(
            'create',
            help='Create a new cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_cluster_inst.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            required=True,
            help="Provide name to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--idle_timeout_ms",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide idle_timeout_ms to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--labels",
            type=check_non_empty_string,
            action='append',
            default=SUPPRESS,
            nargs='+',
            help="Provide labels to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--is_spot_instance",
            type=check_boolean,
            default='false',
            nargs='?',
            choices=['true', 'false'],
            help="Provide is_spot_instance to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--enable_public_ip",
            type=check_boolean,
            default='false',
            nargs='?',
            choices=['true', 'false'],
            help="Provide enable_public_ip to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--block_project_ssh_keys",
            type=check_boolean,
            default='true',
            nargs='?',
            choices=['true', 'false'],
            help="Provide block_project_ssh_keys to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--bootstrap_shell_script_file_path",
            type=check_non_empty_string,
            default=SUPPRESS,
            nargs=1,
            help="Provide bootstrap_shell_script_file_path to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--cloud_env_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide cloud_env_id to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide object_storage_manager_id to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--conf",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--packages",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide packages to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--repositories",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide repositories to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--files",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide files to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--py-files",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide py-files to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--jars",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide jars to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--archives",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide archives to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--env_var",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide env_var to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--conf_secret",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf_secret to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--env_var_secret",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide env_var_secret to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--hive_metastore_conf_id",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide hive_metastore_conf_id to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--spark_infra_version_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide spark_infra_version_id to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--max_parallel_spark_job_execution_per_instance",
            type=int,
            nargs='?',
            default=5,
            help="Provide max_parallel_spark_job_execution_per_instance to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--num_of_workers",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide num_of_workers to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--cluster_type",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            required=True,
            choices=CLUSTER_TYPE_LIST,
            metavar='YEEDU, STANDALONE, CLUSTER',
            help="Provide cluster_type to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--min_instances",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide min_instances to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--max_instances",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide max_instances to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--clean_up_timeout",
            type=int,
            nargs='?',
            default=240,
            help="Provide cleanup_timeout_mins to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide cluster_conf_id to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--keep_scratch_disk",
            type=check_boolean,
            nargs='?',
            default='false',
            choices=['true', 'false'],
            help="Provide keep_scratch_disk to create a cluster instance."
        )
        create_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_cluster_inst = subparser.add_parser(
            'list',
            help='List all available cluster instances.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_cluster_inst.add_argument(
            "--cluster_status",
            type=check_non_empty_string,
            nargs="?",
            default=SUPPRESS,
            help='Provide cluster instance status from ["INITIATING", "RUNNING", "STOPPING", "STOPPED", "DESTROYING", "DESTROYED", "ERROR", "RESIZING_UP", "RESIZING_DOWN"] to list, For example --cluster_status="RUNNING,DESTROYED".'
        )
        list_cluster_inst.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Conf Id to list all the Cluster Instances."
        )
        list_cluster_inst.add_argument(
            "--cluster_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Engine Cluster Config Name to list all the Cluster Instances."
        )
        list_cluster_inst.add_argument(
            "--enable",
            type=check_boolean,
            nargs="?",
            default=SUPPRESS,
            choices=['true', 'false'],
            help="Provide enable as true or false to list the active or disabled Cluster Instances."
        )
        list_cluster_inst.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list cluster instance for a specific page_number."
        )
        list_cluster_inst.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of cluster instance."
        )
        list_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_cluster_inst = subparser.add_parser(
            'search',
            help='Search for cluster instances based on instance name.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_cluster_inst.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide cluster name to search cluster instances."
        )
        search_cluster_inst.add_argument(
            "--cluster_status",
            type=check_non_empty_string,
            nargs="?",
            default=SUPPRESS,
            help='Provide cluster instance status from ["INITIATING", "RUNNING", "STOPPING", "STOPPED", "DESTROYING", "DESTROYED", "ERROR", "RESIZING_UP", "RESIZING_DOWN"] to list, For example --cluster_status="RUNNING,DESTROYED".'
        )
        search_cluster_inst.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Conf Id to list all the Cluster Instances."
        )
        search_cluster_inst.add_argument(
            "--cluster_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Engine Cluster Config Name to list all the Cluster Instances."
        )
        search_cluster_inst.add_argument(
            "--enable",
            type=check_boolean,
            nargs="?",
            default=SUPPRESS,
            choices=['true', 'false'],
            help="Provide enable as true or false to list active or disabled clusters "
        )
        search_cluster_inst.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search cluster instances for a specific page_number."
        )
        search_cluster_inst.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of cluster instances."
        )
        search_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_cluster_inst = subparser.add_parser(
            'get',
            help='Get details of a specific cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance id to get information about a specific cluster instance."
        )
        get_cluster_inst.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance name to get information about a specific cluster instance."
        )
        get_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_cluster_inst = subparser.add_parser(
            'edit',
            help='Modify the configuration of an existing cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific cluster instance id to edit."
        )
        edit_cluster_inst.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific cluster instance name to edit."
        )
        edit_cluster_inst.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--description",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide description to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--idle_timeout_ms",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide idle_timeout_ms to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--labels",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide labels to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--enable_public_ip",
            type=check_boolean,
            nargs='?',
            default=SUPPRESS,
            choices=['true', 'false'],
            help="Provide enable_public_ip to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--block_project_ssh_keys",
            type=check_boolean,
            nargs='?',
            default=SUPPRESS,
            choices=['true', 'false'],
            help="Provide block_project_ssh_keys to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--bootstrap_shell_script_file_path",
            type=validate_string_and_null,
            default=SUPPRESS,
            nargs='?',
            help="Provide bootstrap_shell_script_file_path to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--cloud_env_id",
            type=int,
            default=SUPPRESS,
            nargs='?',
            help="Provide cloud_env_id to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--object_storage_manager_id",
            type=int,
            default=SUPPRESS,
            nargs='?',
            help="Provide object_storage_manager_id to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--hive_metastore_conf_id",
            type=validate_integer_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide hive_metastore_conf_id to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--spark_infra_version_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide spark_infra_version_id to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--cluster_conf_id",
            type=int,
            default=SUPPRESS,
            nargs='?',
            help="Provide cluster_conf_id to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--conf",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--packages",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide packages to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--repositories",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide repositories to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--jars",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide jars to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--archives",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide archives to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--files",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide files to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--py-files",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide py-files to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--env_var",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide env_var to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--conf_secret",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf_secret to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--env_var_secret",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide env_var_secret to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--max_parallel_spark_job_execution_per_instance",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide max_parallel_spark_job_execution_per_instance to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--num_of_workers",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide num_of_workers to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--min_instances",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide min_instances to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--max_instances",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide max_instances to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--clean_up_timeout",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide cleanup_timeout_mins to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--keep_scratch_disk",
            type=check_boolean,
            nargs='?',
            default=SUPPRESS,
            choices=['true', 'false'],
            help="Provide keep_scratch_disk to edit a cluster instance."
        )
        edit_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        start_cluster_inst = subparser.add_parser(
            'start',
            help='Start a specific cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        start_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance id to start a cluster instance."
        )
        start_cluster_inst.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance name to start a cluster instance."
        )
        start_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        start_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        stop_cluster_inst = subparser.add_parser(
            'stop',
            help='Stop a specific cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        stop_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance id to stop a cluster instance."
        )
        stop_cluster_inst.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance name to stop a cluster instance."
        )
        stop_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        stop_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        destroy_cluster_inst = subparser.add_parser(
            'destroy',
            help='Destroy a specific cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        destroy_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance id to destroy a cluster instance."
        )
        destroy_cluster_inst.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance name to destroy a cluster instance."
        )
        destroy_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        destroy_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
        enable_cluster_inst = subparser.add_parser(
            'enable',
            help='Enable a specific cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        enable_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance id to enable a cluster instance."
        )
        enable_cluster_inst.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance name to enable a cluster instance."
        )
        enable_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        enable_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
        disable_cluster_inst = subparser.add_parser(
            'disable',
            help='Disable a specific cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        disable_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance id to disable a cluster instance."
        )
        disable_cluster_inst.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance name to disable a cluster instance."
        )
        disable_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        disable_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )


        get_job_stats_by_cluster_inst = subparser.add_parser(
            'get-stats',
            help='Retrieve Spark job statistics for a specific cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_job_stats_by_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance id to get the spark job statistics of a cluster instance."
        )
        get_job_stats_by_cluster_inst.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster instance name to get the spark job statistics of a cluster instance."
        )
        get_job_stats_by_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_job_stats_by_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_cluster_inst_status = subparser.add_parser(
            'list-status',
            help='List status events for a specific cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_cluster_inst_status.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster id to list all the cluster instance status."
        )
        list_cluster_inst_status.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster name to list all the cluster instance status."
        )
        list_cluster_inst_status.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list the cluster instance status for a specific page_number."
        )
        list_cluster_inst_status.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of cluster instance status."
        )
        list_cluster_inst_status.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_cluster_inst_status.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        stop_all_jobs_of_cluster_inst = subparser.add_parser(
            'stop-all-jobs',
            help='Stops all jobs in a specific cluster that are in the SUBMITTED or RUNNING state.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        stop_all_jobs_of_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Specifies the ID of the cluster instance to stop all the jobs."
        )
        stop_all_jobs_of_cluster_inst.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        stop_all_jobs_of_cluster_inst.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_cluster_errors = subparser.add_parser(
            'list-errors',
            help='List errors for a specific cluster instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_cluster_errors.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide cluster id to list all the cluster errors."
        )
        list_cluster_errors.add_argument(
            "--cluster_status_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Status Id to list all the cluster errors."
        )
        list_cluster_errors.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list all the cluster errors for a specific page_number."
        )
        list_cluster_errors.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of cluster errors."
        )
        list_cluster_errors.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_cluster_errors.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
