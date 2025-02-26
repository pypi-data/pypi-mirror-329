from yeeducli.utility.json_utils import check_boolean, check_non_empty_string
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.constants import SPARK_JOB_TYPE


class ClusterWorkspaceMappingParser:
    def cluster_workspace_mapping_parser(subparser):
        associate_workspace = subparser.add_parser(
            'associate-workspace',
            help='Associate a cluster with a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        associate_workspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to associate it with a cluster."
        )
        associate_workspace.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Cluster Id to to associate it with a workspace."
        )
        associate_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        associate_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        dissociate_workspace = subparser.add_parser(
            'dissociate-workspace',
            help='Dissociate a cluster from a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        dissociate_workspace.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to dissociate it with a cluster."
        )
        dissociate_workspace.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Cluster Id to dissociate it with a workspace."
        )
        dissociate_workspace.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        dissociate_workspace.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_workspaces = subparser.add_parser(
            'list-workspaces',
            help='List all workspaces associated with a cluster.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_workspaces.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Cluster Id to list all the associated workspaces."
        )
        list_workspaces.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Clusters for a specific page_number."
        )
        list_workspaces.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Clusters."
        )
        list_workspaces.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_workspaces.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_workspaces = subparser.add_parser(
            'search-workspaces',
            help='Search workspaces associated with a cluster.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_workspaces.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Cluster Id to list all the associated workspaces."
        )
        search_workspaces.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            nargs="?",
            required=True,
            default=SUPPRESS,
            help="Provide workspace name to search all the workspaces having access to a cluster."
        )
        search_workspaces.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Clusters for a specific page_number."
        )
        search_workspaces.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Clusters."
        )
        search_workspaces.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_workspaces.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_workspace_clusters = subparser.add_parser(
            'list-workspace-clusters',
            help='List all clusters associated with a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_workspace_clusters.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Workspace Id to list all the associated clusters."
        )
        list_workspace_clusters.add_argument(
            "--cluster_status",
            type=check_non_empty_string,
            nargs="?",
            default=SUPPRESS,
            help='Provide Cluster Instance Status from ["INITIATING", "RUNNING", "STOPPING", "STOPPED", "DESTROYING", "DESTROYED", "ERROR", "RESIZING_UP", "RESIZING_DOWN"] to list, For example --cluster_status="RUNNING,DESTROYED".'
        )
        list_workspace_clusters.add_argument(
            "--enable",
            type=check_boolean,
            nargs="?",
            default=SUPPRESS,
            choices=['true', 'false'],
            help="Provide enable as true or false to list the active or disabled Cluster Instances."
        )
        list_workspace_clusters.add_argument(
            "--job_type",
            type=check_non_empty_string,
            nargs="?",
            default=SUPPRESS,
            choices=SPARK_JOB_TYPE,
            help="To list Clusters for a specific job_type."
        )
        list_workspace_clusters.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list Clusters for a specific page_number."
        )
        list_workspace_clusters.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Clusters."
        )
        list_workspace_clusters.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_workspace_clusters.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_workspace_clusters = subparser.add_parser(
            'search-workspace-clusters',
            help='Search clusters associated with a workspace.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_workspace_clusters.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide workspace id to search all the associated clusters."
        )
        search_workspace_clusters.add_argument(
            "--cluster_name",
            type=check_non_empty_string,
            nargs="?",
            default=SUPPRESS,
            required=True,
            help="Provide cluster name to search all the associated workspace clusters."
        )
        search_workspace_clusters.add_argument(
            "--cluster_status",
            type=check_non_empty_string,
            nargs="?",
            default=SUPPRESS,
            help='Provide cluster instance status from ["INITIATING", "RUNNING", "STOPPING", "STOPPED", "DESTROYING", "DESTROYED", "ERROR", "RESIZING_UP", "RESIZING_DOWN"] to search, for example --cluster_status="RUNNING,DESTROYED".'
        )
        search_workspace_clusters.add_argument(
            "--enable",
            type=check_boolean,
            nargs="?",
            default=SUPPRESS,
            choices=['true', 'false'],
            help="Provide enable as true or false to list the active or disabled Cluster Instances."
        )
        search_workspace_clusters.add_argument(
            "--job_type",
            type=check_non_empty_string,
            nargs="?",
            default=SUPPRESS,
            choices=SPARK_JOB_TYPE,
            help="To search clusters of a specific job_type."
        )
        search_workspace_clusters.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To search clusters for a specific page_number."
        )
        search_workspace_clusters.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to search number of clusters."
        )
        search_workspace_clusters.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_workspace_clusters.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
