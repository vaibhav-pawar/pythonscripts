########################################################
# ...........Module for Base configurations........... #
# ..that will be used in rest of the code frequently.. #
########################################################
import logging
import os
import time
from base_imports import *


# Default Paths
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
BACKEND_PATH = f"{BASE_PATH}/backend"
FILES_PATH = os.path.abspath(os.path.join(BACKEND_PATH, "./Files"))
REPORT_PATH = os.path.abspath(os.path.join(BACKEND_PATH, "./Report"))
LIVE_REPORT_PATH = os.path.join(REPORT_PATH, "Live Report")
MONTHLY_REPORT_PATH = os.path.join(REPORT_PATH, "Monthly Reports")
DAILY_REPORT_PATH = os.path.join(REPORT_PATH, "Daily Reports")
LOGS_PATH = os.path.abspath(os.path.join(BACKEND_PATH, "./Logs"))

# Default File Locations
CONFIG_FILE = os.path.abspath(os.path.join(BACKEND_PATH, "./baseConfig/config.json"))
SECRET_KEY_FILE = os.path.abspath(os.path.join(BACKEND_PATH, "./baseConfig/secret.key"))
EMAIL_CREDENTIALS = os.path.abspath(os.path.join(BACKEND_PATH, "./baseConfig/email_credentials.json"))
ORG_DEVICE_STATUS_FILE = f"{FILES_PATH}/org_devices_status.json"
ORG_DEVICES = f"{FILES_PATH}/org_devices.json"
ORG_NETWORKS_FILE = f"{FILES_PATH}/org_networks.json"
MAPPER_FILE = f"{FILES_PATH}/mapper.json"
SLA_JSON_FILE = f"{FILES_PATH}/device_sla.json"
MAINTENANCE_MAPPER_FILE = f"{FILES_PATH}/maintenance_mapper.json"
START_DATETIME_FILE = f"{FILES_PATH}/ engine_start_datetime.json"
LOGS_FILE = f"{LOGS_PATH}/logs.txt"

# Default Email address for notifications.
EMAIL_ADDRESS = "automation.meraki@gmail.com"

# Script execution Interval.
EXECUTION_INTERVAL = 90
LAST_DAYS_MAPPING = [(1, 31), (2, 28), (3, 31), (4, 30), (5, 31), (6, 30),
                     (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31)]

# Default Names
NETWORK_WISE_REPORT_NAME = "availability_report_network_wise.xlsx"
SINGLE_AVAILABILITY_REPORT_NAME = "availability_report.xlsx"
SINGLE_AVAILABILITY_REPORT_WITH_MAINTENANCE_NAME = "availability_report_with_maintenance.xlsx"
LIVE_REPORT_FILE = f"{LIVE_REPORT_PATH}/{SINGLE_AVAILABILITY_REPORT_NAME}"


# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
try:
    file_handler = logging.FileHandler(f"{LOGS_PATH}/runtime.log")
except FileNotFoundError:
    os.mkdir(LOGS_PATH)
    file_handler = logging.FileHandler(f"{LOGS_PATH}/runtime.log")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
