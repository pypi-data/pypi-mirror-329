from yeeducli.constants import CONFIG_FILE_PATH
from dotenv import load_dotenv
from urllib.parse import urljoin
import os
import json
import warnings
import urllib3

warnings.filterwarnings(
    "ignore", category=urllib3.exceptions.InsecureRequestWarning)

load_dotenv()


YEEDU_RESTAPI_URL = urljoin(
    os.getenv("YEEDU_RESTAPI_URL", "http://localhost:8080"), "api/v1")

YEEDU_RESTAPI_TOKEN = ''

if (os.getenv("YEEDU_RESTAPI_TOKEN") is not None):

    YEEDU_RESTAPI_TOKEN = os.getenv("YEEDU_RESTAPI_TOKEN")

elif os.path.isfile(CONFIG_FILE_PATH):

    with open(f"{CONFIG_FILE_PATH}", "r") as configfile:
        cli_token = json.load(configfile)
        configfile.close()

        YEEDU_RESTAPI_TOKEN = cli_token["token"]

header_without_auth = {
    'Content-Type': 'application/json',
    'accept': '*/*'
}

headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {YEEDU_RESTAPI_TOKEN}"
}

headers_files = {
    'accept': '*/*',
    'Content-Type': 'application/octet-stream',
    'Authorization': f"Bearer {YEEDU_RESTAPI_TOKEN}"
}
