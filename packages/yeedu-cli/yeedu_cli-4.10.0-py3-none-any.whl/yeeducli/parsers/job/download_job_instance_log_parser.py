from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string


class DownloadJobInstanceLogParser:

    def download_job_instance_log_parser(subparser):

        download_Job_instance_logs = subparser.add_parser(
            'logs',
            help='To download Spark Job Instance logs by job id.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        download_Job_instance_logs.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide workspace_id to download Spark Job Instance log records."
        )
        download_Job_instance_logs.add_argument(
            "--job_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide job_id to download Spark Job Instance log records."
        )
        download_Job_instance_logs.add_argument(
            "--log_type",
            type=check_non_empty_string,
            nargs=1,
            default='stdout',
            choices=['stdout', 'stderr'],
            help="Provide log_type to download Spark Job Instance log records."
        )
        download_Job_instance_logs.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        download_Job_instance_logs.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
