from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null, validate_integer_and_null, validate_array_of_intgers, check_choices
from yeeducli.constants import CREATE_JOB_TYPE_LANG, SPARK_JOB_TYPE_LANG_FOR_CONF, SPARK_JOB_STATUS, SPARK_JOB_TYPE_FOR_CONF
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter

class SparkJobConfigurationParser:

    def spark_job_configuration_parser(subparser):

        create_spark_job_conf = subparser.add_parser(
            'create-conf',
            help='To create the Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_spark_job_conf.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_id to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_name to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--files",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide files to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--properties-file",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide properties-file to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--conf",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--packages",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide packages to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--repositories",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide repositories to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--jars",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide jars to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--archives",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide archives to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-memory",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-memory to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-java-options",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-java-options to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-library-path",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-library-path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-class-path",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-class-path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--executor-memory",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-memory to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-cores to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--total-executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide total-executor-cores to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-cores to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--num-executors",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide num-executors to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--principal",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide principal to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--keytab",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide keytab to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--queue",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide queue to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-class-name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-class-name to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-command",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-command to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-arguments",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-arguments to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-raw-scala-code",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide job-raw-scala-code file path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-type",
            type=check_non_empty_string,
            default=SUPPRESS,
            choices=CREATE_JOB_TYPE_LANG,
            required=True,
            help="Provide job-type to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--job-timeout-min",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide job-timeout-min to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--max_concurrency",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide max_concurrency number to limit the number of jobs submitted."
        )
        create_spark_job_conf.add_argument(
            "--yeedu-functions-project-path",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-project-path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--yeedu-functions-script-path",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-script-path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--yeedu-functions-function-name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide yeedu-functions-function-name to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--yeedu-functions-requirements",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-requirements to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--yeedu-functions-max-request-concurrency",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-max-request-concurrency to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--yeedu-functions-request-timeout-sec",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-request-timeout-sec to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--yeedu-functions-idle-timeout-sec",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-idle-timeout-sec to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--yeedu-functions-example-request-body",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-example-request-body to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
        list_spark_job_conf = subparser.add_parser(
            'list-confs',
            help='To list all the available Job Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="To list Job Configurations of a specific workspace."
        )
        list_spark_job_conf.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable as true or false to list Job Configurations of a specific workspace."
        )
        list_spark_job_conf.add_argument(
            "--cluster_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of cluster instance IDs to filter on."
        )
        list_spark_job_conf.add_argument(
            "--job_type",
            type=lambda values: check_choices(
                values, choices=SPARK_JOB_TYPE_FOR_CONF),
            nargs='?',
            default=SUPPRESS,
            help="An optional set of job types filter for Spark job configurations. Choices are: " +
            ", ".join(SPARK_JOB_TYPE_FOR_CONF)
        )
        list_spark_job_conf.add_argument(
            "--job_type_langs",
            type=lambda values: check_choices(values, choices=SPARK_JOB_TYPE_LANG_FOR_CONF),
            nargs='?',
            default=SUPPRESS,
            help="An optional set of language filter for Spark job configurations. Choices are: " +
            ", ".join(SPARK_JOB_TYPE_LANG_FOR_CONF)
        )
        list_spark_job_conf.add_argument(
            "--last_run_status",
            type=lambda values: check_choices(
                values, choices=SPARK_JOB_STATUS),
            nargs='?',
            default=SUPPRESS,
            help="An optional set of last run statuses to filter Spark job configurations. Choices are: " +
            ", ".join(SPARK_JOB_STATUS)
        )
        list_spark_job_conf.add_argument(
            "--created_by_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of created by user IDs to filter on."
        )
        list_spark_job_conf.add_argument(
            "--modified_by_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of modified by user IDs to filter on."
        )
        list_spark_job_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Job Configurations for a specific page_number."
        )
        list_spark_job_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Job Configurations."
        )
        list_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_job_confs = subparser.add_parser(
            'search-confs',
            help='To search job configurations by job conf name in a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_job_confs.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to search job configurations in it."
        )
        search_job_confs.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide job_conf_name to search job configurations."
        )
        search_job_confs.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable as true or false to search job configurations."
        )
        search_job_confs.add_argument(
            "--cluster_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of cluster instance IDs to filter on."
        )
        search_job_confs.add_argument(
            "--job_type",
            type=lambda values: check_choices(
                values, choices=SPARK_JOB_TYPE_FOR_CONF),
            nargs='?',
            default=SUPPRESS,
            help="An optional set of job types filter for Spark job configurations. Choices are: " +
            ", ".join(SPARK_JOB_TYPE_FOR_CONF)
        )
        search_job_confs.add_argument(
            "--job_type_langs",
            type=lambda values: check_choices(values, choices=SPARK_JOB_TYPE_LANG_FOR_CONF),
            nargs='?',
            default=SUPPRESS,
            help="An optional set of language filter for Spark job configurations. Choices are: " +
            ", ".join(SPARK_JOB_TYPE_LANG_FOR_CONF)
        )
        search_job_confs.add_argument(
            "--last_run_status",
            type=lambda values: check_choices(
                values, choices=SPARK_JOB_STATUS),
            nargs='?',
            default=SUPPRESS,
            help="An optional set of last run statuses to filter Spark job configurations. Choices are: " +
            ", ".join(SPARK_JOB_STATUS)
        )
        search_job_confs.add_argument(
            "--created_by_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of created by user IDs to filter on."
        )
        search_job_confs.add_argument(
            "--modified_by_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of modified by user IDs to filter on."
        )
        search_job_confs.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search job configurations for a specific page_number."
        )
        search_job_confs.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of job configurations."
        )
        search_job_confs.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_job_confs.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        describe_spark_job_conf = subparser.add_parser(
            'get-conf',
            help='To get the information about a specific Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to get information about a specific Spark Job Configuration."
        )
        describe_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Id to get information about a specific Spark Job Configuration."
        )
        describe_spark_job_conf.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config name to get information about a specific Spark Job Configuration."
        )
        describe_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        describe_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_spark_job_conf = subparser.add_parser(
            'edit-conf',
            help='To edit the Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Id to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Name to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_id to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_name to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--files",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide files to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--properties-file",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide properties-file to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--conf",
            type=validate_string_and_null,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--packages",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide packages to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--repositories",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide repositories to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--jars",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide jars to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--archives",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide archives to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-memory",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-memory to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-java-options",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-java-options to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-library-path",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-library-path to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-class-path",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-class-path to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--executor-memory",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-memory to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-cores",
            type=validate_integer_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-cores to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--total-executor-cores",
            type=validate_integer_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide total-executor-cores to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--executor-cores",
            type=validate_integer_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-cores to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--num-executors",
            type=validate_integer_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide num-executors to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--principal",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide principal to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--keytab",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide keytab to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--queue",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide queue to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job-class-name",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-class-name to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide name to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job-command",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-command to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job-arguments",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide job-arguments to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job-raw-scala-code",
            type=validate_string_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide job-raw-scala-code file path to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job-timeout-min",
            type=validate_integer_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Provide job-timeout-min to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--max_concurrency",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide max_concurrency number to limit the number of jobs submitted."
        )
        #yeedu_functions arguments
        edit_spark_job_conf.add_argument(
            "--yeedu-functions-project-path",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-project-path to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--yeedu-functions-script-path",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-script-path to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--yeedu-functions-function-name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide yeedu-functions-function-name to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--yeedu-functions-requirements",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-requirements to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--yeedu-functions-max-request-concurrency",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-max-request-concurrency to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--yeedu-functions-request-timeout-sec",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-request-timeout-sec to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--yeedu-functions-idle-timeout-sec",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-idle-timeout-sec to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--yeedu-functions-example-request-body",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide yeedu-functions-example-request-body to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        enable_spark_job_conf = subparser.add_parser(
            'enable-conf',
            help='To enable a specific Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        enable_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to enable the Spark Job Configuration."
        )
        enable_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Id to enable the Spark Job Configuration."
        )
        enable_spark_job_conf.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Name to enable the Spark Job Configuration."
        )
        enable_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        enable_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        disable_spark_job_conf = subparser.add_parser(
            'disable-conf',
            help='To disable a specific Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        disable_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to disable the Spark Job Configuration."
        )
        disable_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Id to disable the Spark Job Configuration."
        )
        disable_spark_job_conf.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Name to disable the Spark Job Configuration."
        )
        disable_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        disable_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        export_spark_job_conf = subparser.add_parser(
            'export',
            help='Export a specific Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        export_spark_job_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to export a specific Spark Job Configuration from it."
        )
        export_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config Id to export a specific Spark Job Configuration."
        )
        export_spark_job_conf.add_argument(
            "--job_conf_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Config name to export a specific Spark Job Configuration."
        )
        export_spark_job_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        export_spark_job_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
