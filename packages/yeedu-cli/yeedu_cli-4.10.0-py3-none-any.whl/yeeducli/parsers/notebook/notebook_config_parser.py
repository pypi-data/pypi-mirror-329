from yeeducli.constants import NOTEBOOK_LANGUAGE_LIST, NOTEBOOK_LANG, SPARK_JOB_STATUS
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_integer_and_null, validate_string_and_null, validate_array_of_intgers, check_choices
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class NotebookConfigurationParser:

    def notebook_configuration_parser(subparser):

        create_notebook_conf = subparser.add_parser(
            'create-conf',
            help='To create a Notebook Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_notebook_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_id to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_name to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--notebook_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide notebook_name to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--notebook_type",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            metavar='python3,scala',
            choices=NOTEBOOK_LANGUAGE_LIST,
            required=True,
            help="Provide notebook type to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--conf",
            type=check_non_empty_string,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--files",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide files to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--jars",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide jars to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--packages",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide packages to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--driver-memory",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-memory to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--executor-memory",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-memory to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--driver-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-cores to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--total-executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide total-executor-cores to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-cores to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--num-executors",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide num-executors to create a Notebook Configuration."
        )
        create_notebook_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_notebook_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_notebook_conf = subparser.add_parser(
            'list-confs',
            help='To list all the available Notebook Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_notebook_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="To list Notebook Configurations of a specific workspace."
        )
        list_notebook_conf.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable as true or false to list Notebook Configurations of a specific workspace."
        )
        list_notebook_conf.add_argument(
            "--cluster_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of cluster instance IDs to filter on."
        )
        list_notebook_conf.add_argument(
            "--language",
            type=lambda values: check_choices(values, choices=NOTEBOOK_LANG),
            nargs='?',
            default=SUPPRESS,
            help="An optional set of language filter for notebook configurations. Choices are: " +
            ", ".join(NOTEBOOK_LANG)
        )
        list_notebook_conf.add_argument(
            "--last_run_status",
            type=lambda values: check_choices(
                values, choices=SPARK_JOB_STATUS),
            nargs='?',
            default=SUPPRESS,
            help="An optional set of last run statuses to filter notebook configurations. Choices are: " +
            ", ".join(SPARK_JOB_STATUS)
        )
        list_notebook_conf.add_argument(
            "--created_by_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of created by user IDs to filter on."
        )
        list_notebook_conf.add_argument(
            "--modified_by_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of modified by user IDs to filter on."
        )
        list_notebook_conf.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Notebook Configurations for a specific page_number."
        )
        list_notebook_conf.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Notebook Configurations."
        )
        list_notebook_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_notebook_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_notebook_confs = subparser.add_parser(
            'search-confs',
            help='To search Notebook Configurations by notebook name in a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_notebook_confs.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to search Notebook Configurations in it."
        )
        search_notebook_confs.add_argument(
            "--notebook_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide notebook_name to search Notebook Configurations."
        )
        search_notebook_confs.add_argument(
            "--enable",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default=SUPPRESS,
            help="Provide enable as true or false to search Notebook Configurations."
        )
        search_notebook_confs.add_argument(
            "--cluster_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of cluster instance IDs to filter on."
        )
        search_notebook_confs.add_argument(
            "--language",
            type=lambda values: check_choices(values, choices=NOTEBOOK_LANG),
            nargs='?',
            default=SUPPRESS,
            help="An optional set of language filter for notebook configurations. Choices are: " +
            ", ".join(NOTEBOOK_LANG)
        )
        search_notebook_confs.add_argument(
            "--last_run_status",
            type=lambda values: check_choices(
                values, choices=SPARK_JOB_STATUS),
            nargs='?',
            default=SUPPRESS,
            help="An optional set of last run statuses to filter notebook configurations. Choices are: " +
            ", ".join(SPARK_JOB_STATUS)
        )
        search_notebook_confs.add_argument(
            "--created_by_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of created by user IDs to filter on."
        )
        search_notebook_confs.add_argument(
            "--modified_by_ids",
            type=validate_array_of_intgers,
            nargs='?',
            default=SUPPRESS,
            help="An optional set of modified by user IDs to filter on."
        )
        search_notebook_confs.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search Notebook Configurations for a specific page_number."
        )
        search_notebook_confs.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of Notebook Configurations."
        )
        search_notebook_confs.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_notebook_confs.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        get_notebook_conf = subparser.add_parser(
            'get-conf',
            help='To get the information about a specific Notebook Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_notebook_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to get information about a specific Notebook Configuration."
        )
        get_notebook_conf.add_argument(
            "--notebook_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Notebook Conf Id to get information about a specific Notebook Configuration."
        )
        get_notebook_conf.add_argument(
            "--notebook_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Notebook Name to get information about a specific Notebook Configuration."
        )
        get_notebook_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        get_notebook_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        edit_notebook_conf = subparser.add_parser(
            'edit-conf',
            help='To edit the Notebook Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_notebook_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--notebook_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Notbeook Conf Id to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--notebook_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Notebook Name to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_id to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide cluster_name to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--name",
            type=check_non_empty_string,
            nargs='?',
            default=SUPPRESS,
            help="Provide name to edit notebook_name of a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--conf",
            type=validate_string_and_null,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--files",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide files to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--jars",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide jars to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--packages",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide packages to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--driver-memory",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-memory to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--executor-memory",
            type=validate_string_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-memory to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--driver-cores",
            type=validate_integer_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-cores to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--total-executor-cores",
            type=validate_integer_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide total-executor-cores to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--executor-cores",
            type=validate_integer_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-cores to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--num-executors",
            type=validate_integer_and_null,
            nargs='?',
            default=SUPPRESS,
            help="Provide num-executors to edit a Notebook Configuration."
        )
        edit_notebook_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        edit_notebook_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        enable_notebook_conf = subparser.add_parser(
            'enable-conf',
            help='To enable a specific Notebook Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        enable_notebook_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to enable the Notebook Configuration."
        )
        enable_notebook_conf.add_argument(
            "--notebook_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Notebook Conf Id to enable the Notebook Configuration."
        )
        enable_notebook_conf.add_argument(
            "--notebook_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Notebook Name to enable the Notebook Configuration."
        )
        enable_notebook_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        enable_notebook_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        disable_notebook_conf = subparser.add_parser(
            'disable-conf',
            help='To disable a specific Notebook Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        disable_notebook_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to disable the Notebook Configuration."
        )
        disable_notebook_conf.add_argument(
            "--notebook_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Notebook Conf Id to disable the Notebook Configuration."
        )
        disable_notebook_conf.add_argument(
            "--notebook_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Notebook Name to disable the Notebook Configuration."
        )
        disable_notebook_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        disable_notebook_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        export_notebook_conf = subparser.add_parser(
            'export',
            help='Export a specific Notebook Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        export_notebook_conf.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace id to export a specific Notebook Configuration from it."
        )
        export_notebook_conf.add_argument(
            "--notebook_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Notebook Config Id to export a specific Notebook Configuration."
        )
        export_notebook_conf.add_argument(
            "--notebook_name",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide Notebook name to export a specific Notebook Configuration."
        )
        export_notebook_conf.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        export_notebook_conf.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
