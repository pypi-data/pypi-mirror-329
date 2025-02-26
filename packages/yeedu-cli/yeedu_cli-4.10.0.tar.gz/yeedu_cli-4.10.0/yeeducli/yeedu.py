#!/usr/bin/env python3

from yeeducli.parsers.configure.configure_user_parser import ConfigureUserParser
from yeeducli.subcommand_module.service_subcommand import ServiceSubcommand
from yeeducli.parsers.service_parser import ServiceParser
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.json_utils import *
from argparse import ArgumentParser, SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.constants import *
import sys

logger = Logger.get_logger(__name__, True)


def yeedu():

    try:
        if len(sys.argv) > 1:
            if sys.argv[1] in COMMANDS_DICT.keys():
                try:
                    if (sys.argv[2] in COMMANDS_DICT[sys.argv[1]]) or (sys.argv[2] in ['-h', '--help']):
                        parser, subparser = main_parser(sys.argv[1])
                        ServiceParser.create_service_parser(
                            sys.argv[1], subparser)
                        call_service_subcommand(parser)
                    else:
                        logger.error(
                            f"Please provide \"yeedu {sys.argv[1]} [{sys.argv[1]}-service]\"\n")
                        logger.error(get_similar_subcommand(
                            sys.argv[2], COMMANDS_DICT[sys.argv[1]]))
                        sys.exit(-1)
                except IndexError as e:
                    logger.error(
                        f"Please provide \"yeedu {sys.argv[1]} [-h] [{sys.argv[1]}-services]\"\n")
                    sys.exit(-1)

            elif sys.argv[1] in ['configure', 'logout']:
                try:
                    parser = main_parser(sys.argv[1])
                    ConfigureUserParser.configure_user_parser(parser)
                    call_service_subcommand(parser)

                except IndexError as e:
                    logger.error(
                        f"Please provide \"yeedu {sys.argv[1]} [-h] [{sys.argv[1]}-options]\"\n")
                    sys.exit(-1)

            elif sys.argv[1] in ['-h', '--help']:
                logger.info(
                    """\nusage:\tyeedu [-h]\n\tyeedu configure [-h] [configure-options]\n\tyeedu resource [-h] [resource-services]\n\tyeedu cluster [-h] [cluster-services]\n\tyeedu workspace [-h] [workspace-services]\n\tyeedu job [-h] [job-services]\n\tyeedu notebook [-h] [notebook-services]\n\tyeedu billing [-h] [billing-services]\n\tyeedu iam [-h] [iam-services]\n\tyeedu admin [-h] [admin-services]\n\tyeedu platform-admin [-h] [platform-admin-services]\n\tyeedu logout [-h] [logout-options]\n""")

            else:
                logger.error(
                    f"""\nusage:\tyeedu [-h]\n\tyeedu configure [-h] [configure-options]\n\tyeedu resource [-h] [resource-services]\n\tyeedu cluster [-h] [cluster-services]\n\tyeedu workspace [-h] [workspace-services]\n\tyeedu job [-h] [job-services]\n\tyeedu notebook [-h] [notebook-services]\n\tyeedu billing [-h] [billing-services]\n\tyeedu iam [-h] [iam-services]\n\tyeedu admin [-h] [admin-services]\n\tyeedu platform-admin [-h] [platform-admin-services]\n\tyeedu logout [-h] [logout-options]\n\nyeedu: error: argument command: '{sys.argv[1]}' is invalid. \n\nValid choices are:\n configure | resource | cluster | workspace | job | notebook | billing | iam | admin | platform-admin | logout""")
        else:
            logger.error(
                """\nusage:\tyeedu [-h]\n\tyeedu configure [-h] [configure-options]\n\tyeedu resource [-h] [resource-services]\n\tyeedu cluster [-h] [cluster-services]\n\tyeedu workspace [-h] [workspace-services]\n\tyeedu job [-h] [job-services]\n\tyeedu notebook [-h] [notebook-services]\n\tyeedu billing [-h] [billing-services]\n\tyeedu iam [-h] [iam-services]\n\tyeedu admin [-h] [admin-services]\n\tyeedu platform-admin [-h] [platform-admin-services]\n\tyeedu logout [-h] [logout-options]\n""")
            sys.exit(-1)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def main_parser(service):
    try:
        parser = ArgumentParser(
            description="Yeedu CLI",
            usage=SUPPRESS,
            add_help=False,
            formatter_class=ArgumentDefaultsHelpFormatter
        )

        parser.add_argument(
            "yeedu",
            type=str,
            choices=[service]
        )
        parser.add_argument(
            '-h', '--help',
            action='help',
            default=SUPPRESS,
            help='Show this help message and exit.'
        )

        if service in ['configure', 'logout']:
            return parser
        else:
            subparser = parser.add_subparsers(dest='subcommand')
            return parser, subparser

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def call_service_subcommand(parser):
    try:
        args = parser.parse_args()

        if args.yeedu in ['configure', 'logout']:
            ServiceSubcommand.call_configure_service_subcommand(args)
        elif args.subcommand in RESOURCE_LIST and args.yeedu == 'resource':
            ServiceSubcommand.call_resource_service_subcommand(args)
        elif args.subcommand in CLUSTER_LIST and args.yeedu == 'cluster':
            ServiceSubcommand.call_cluster_service_subcommand(args)
        elif args.subcommand in WORKSPACE_LIST and args.yeedu == 'workspace':
            ServiceSubcommand.call_workspace_service_subcommand(args)
        elif args.subcommand in JOB_LIST and args.yeedu == 'job':
            ServiceSubcommand.call_job_service_subcommand(args)
        elif args.subcommand in NOTEBOOK_LIST and args.yeedu == 'notebook':
            ServiceSubcommand.call_notebook_service_subcommand(args)
        elif args.subcommand in BILLING_LIST and args.yeedu == 'billing':
            ServiceSubcommand.call_billing_service_subcommand(args)
        elif args.subcommand in IAM_LIST and args.yeedu == 'iam':
            ServiceSubcommand.call_iam_service_subcommand(args)
        elif args.subcommand in ADMIN_LIST and args.yeedu == 'admin':
            ServiceSubcommand.call_common_platform_and_admin_service_subcommand(
                args)
        elif args.subcommand in PLATFORM_ADMIN_LIST and args.yeedu == 'platform-admin':
            ServiceSubcommand.call_common_platform_and_admin_service_subcommand(
                args)
        else:
            logger.error(
                f"yeedu: error: argument command:'{args.subcommand}' not found in any yeedu services.")
            sys.exit(-1)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


if __name__ == '__main__':
    yeedu()
