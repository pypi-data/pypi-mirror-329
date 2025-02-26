from yeeducli.constants import DEFAULT_CLI_LOG_PATH, YEEDU_CLI_MAX_LOG_FILES, YEEDU_CLI_MAX_LOG_FILE_SIZE
from dotenv import load_dotenv
from os.path import join
import os
import logging
from logging.handlers import RotatingFileHandler
import sys

load_dotenv()


class Logger:
    def get_logger(logger_name, create_file=False):

        # create logger for yeedu logs.
        logger = logging.getLogger(logger_name)

        logger.setLevel(level=logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        try:
            if create_file:

                # create file handler for yeedu logs.
                filename = 'yeedu_cli_logs.log'
                if os.getenv('YEEDU_CLI_LOG_DIR'):
                    os.makedirs(os.getenv('YEEDU_CLI_LOG_DIR'),
                                mode=0o777, exist_ok=True)
                    yeedu_logs_path = join(
                        os.getenv('YEEDU_CLI_LOG_DIR'), filename)

                elif not os.getenv('YEEDU_CLI_LOG_DIR'):

                    os.makedirs(DEFAULT_CLI_LOG_PATH,
                                mode=0o777, exist_ok=True)
                    yeedu_logs_path = join(DEFAULT_CLI_LOG_PATH, filename)

                # add log retention handlers
                handler = RotatingFileHandler(
                    yeedu_logs_path,
                    mode="a",
                    maxBytes=YEEDU_CLI_MAX_LOG_FILE_SIZE * 1024 * 1024,  # default 30 MB in Bytes
                    backupCount=YEEDU_CLI_MAX_LOG_FILES  # default 5 number of files
                )

                handler.setFormatter(formatter)

            # create console handler for logger.
            ch = logging.StreamHandler(stream=sys.stdout)
            ch.setLevel(level=logging.INFO)
            # ch.setFormatter(formatter)

            # add handlers to logger.
            if create_file:
                logger.addHandler(handler)

            logger.addHandler(ch)

        except Exception as e:
            logger.exception(e)
            sys.exit(-1)

        return logger
