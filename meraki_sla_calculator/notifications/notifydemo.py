from backend.baseConfig.config import *
from backend.engine.helpers import read, write, strp_dtime, get_password
from datetime import datetime
from time import sleep
from backend.baseConfig.html_templates import *

# Track the sla file every 5 minutes.
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
TRACKER_PATH = os.path.abspath(os.path.join(BASE_PATH, "./Tracker"))
TRACKER_FILE = f"{TRACKER_PATH}/tracker.json"
TRACKER_LOG_FILE = f"{TRACKER_PATH}/demo_notifications.log"
SCRIPT_STOPPED_SUBJECT = 'Error Notification: [v0.2] Meraki Availability Script has stopped working at'
SCRIPT_STARTED_AGAIN_SUBJECT = 'Notification: [v0.2] Meraki Availability Script has started working again at'



TEST_SUBJECT = 'Test Notification for Meraki Availability Script'
INTERVAL = 30
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")

try:
    file_handler = logging.FileHandler(TRACKER_LOG_FILE)
except FileNotFoundError:
    logger.info("No Tracker Path found. Creating it.")
    os.mkdir(TRACKER_PATH)
    file_handler = logging.FileHandler(TRACKER_LOG_FILE)
    sleep(1)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

try:
    tracker = read(TRACKER_FILE)
except FileNotFoundError:
    logger.info("No Tracker file found in Tracker Path, Creating it..")
    write(TRACKER_FILE, {})
    sleep(1)

while True:
    print("LIVE_REPORT_FILE: ", LIVE_REPORT_FILE)
    print("TRACKER_FILE: ", TRACKER_FILE)
    print("BASE_PATH: ", BASE_PATH)
    logger.info("Polling Started..")
    sleep(1)
    # Read tracker file
    tracker: dict = read(TRACKER_FILE)
    # Get updated time of file.
    # last_changed_time = os.stat(ORG_DEVICE_STATUS_FILE).st_atime
    last_changed_time = os.stat(LIVE_REPORT_FILE).st_mtime
    print("New_time:", datetime.fromtimestamp(os.stat(LIVE_REPORT_FILE).st_mtime))
    print("Last Time: ", datetime.fromtimestamp(tracker["latest_changed_time"]))

    try:
        # If time is greater than last changed time that file has updated. Script is running..
        print("****Checking last changed time")
        if last_changed_time > tracker["latest_changed_time"]:
            logger.info("Script is running. No attention needed.")
            print("****Script is running. No attention needed")
            tracker.update({"latest_changed_time": last_changed_time})
            if tracker["success_email_flag"] == "false":
                """send_error_notification(subject=f"{SCRIPT_STARTED_AGAIN_SUBJECT} "
                                                f"{datetime.fromtimestamp(last_changed_time).strftime('%m/%d/%Y, %H:%M:%S')} IST",
                                        content=SCRIPT_STARTED_AGAIN, password=get_password())"""
                logger.info("Success Email Sent")
                tracker.update({"success_email_flag": "true"})
            try:
                tracker.pop("last_notification_sent_time")
            except KeyError:
                pass
            write(TRACKER_FILE, tracker)
            sleep(1)

        # If time is same as last changed time that file has not updated. Script is stopped.
        elif last_changed_time == tracker["latest_changed_time"]:
            logger.critical("Script is not running.!!!!!!!!!! Attention required Immediately.!!!!")
            sleep(1)
            logger.info("Entering notifications code..")
            try:
                logger.info("Checking when was the last notification sent.")
                last_notification_sent_time = strp_dtime(tracker["last_notification_sent_time"])
                # Compare the interval of last notification time with present time.
                # If difference is greater than 60 minutes than again sent a notification
                if (datetime.now().timestamp() - last_notification_sent_time.timestamp()) / 60 > 60:
                    print(datetime.now().timestamp() - last_notification_sent_time.timestamp())
                    logger.info("Last notification was sent 1 hour ago. Sending notification again.")
                    """send_error_notification(
                        subject=f"{SCRIPT_STOPPED_SUBJECT} {datetime.fromtimestamp(last_changed_time)} IST",
                        content=SCRIPT_STOPPED, password=get_password())"""
                    tracker.update({"last_notification_sent_time": str(datetime.now()),
                                    "success_email_flag": "false"})
                    write(TRACKER_FILE, tracker)
                    sleep(1)

                else:
                    difference = (datetime.now().timestamp() - last_notification_sent_time.timestamp())
                    logger.info(
                        f"Last Notification interval is not more than 1 hour ({difference / 60} minutes). Skipping it..")
                    sleep(1)
            except KeyError:
                logger.info("No notifications sent yet. Hence sending first notification")
                """send_error_notification(
                    subject=f"{SCRIPT_STOPPED_SUBJECT} {datetime.fromtimestamp(last_changed_time)} IST",
                    content=SCRIPT_STOPPED, password=get_password())"""
                tracker.update({"last_notification_sent_time": str(datetime.now()),
                                "success_email_flag": "false"})
                write(TRACKER_FILE, tracker)

                sleep(1)
    except KeyError:
        logger.info("No data captured yet for latest_changed_time. Creating the data")
        tracker.update({"latest_changed_time": last_changed_time,
                        "success_email_flag": "true"})
        write(TRACKER_FILE, tracker)
        sleep(1)
    logger.info(f"Finished polling the script. Sleeping for {INTERVAL / 60} minutes")
    sleep(INTERVAL)
