from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class DownloadNotebookInstanceLogParser:

    def download_notebook_instance_log_parser(subparser):

        download_notebook_instance_logs = subparser.add_parser(
            'logs',
            help='To download Notebook Instance logs.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        download_notebook_instance_logs.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Workspace Id to download Notebook Instance logs."
        )
        download_notebook_instance_logs.add_argument(
            "--notebook_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Notebook Id to download Notebook Instance logs."
        )
        download_notebook_instance_logs.add_argument(
            "--log_type",
            type=check_non_empty_string,
            nargs=1,
            default='stdout',
            choices=['stdout', 'stderr'],
            help="Provide log type to download Notebook Instance logs."
        )
        download_notebook_instance_logs.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        download_notebook_instance_logs.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
