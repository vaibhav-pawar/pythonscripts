from backend.engine.helpers import *
import requests


def check_file(file, _json=True, content=None):
    """
    This method will check if the file exist. If not it will create it.
    :param content:
    :param file: Specify the file name
    :param _json: JSON Bool will decide if file is of type JSON or plain text file.
    :return: None
    """
    if content is None:
        content = {}
    try:
        read(file)
    except FileNotFoundError:
        if _json:
            write(file, content)
        else:
            write(file, "")


ALERTING_FiLE = "alerting_devices.json"
REFERENCE_FiLE = "reference.json"
check_file(REFERENCE_FiLE, content=[])
check_file(ALERTING_FiLE)




def get_alerting_devices():
    print("Getting Alerting device List..")
    alerting_devices = []
    config_file = read(CONFIG_FILE)
    devices_status = get_org_devices_status(org=config_file[0])
    org_status_file = write("test_org_status_file.json", devices_status)
    devices = read("test_org_status_file.json")

    for device in devices:
        if device["status"] == "alerting":
            if device["serial"] in read(SLA_JSON_FILE):
                alerting_devices.append(device)
    return alerting_devices


def remove_alerting_devices():
    print("Removing Online devices..")
    alerting_devices_file: dict = read(ALERTING_FiLE)
    reference_file: list = read(REFERENCE_FiLE)
    devices = read("test_org_status_file.json")
    for device, attrb in list(alerting_devices_file.items()):
        for org_device in devices:
            if org_device["serial"] == device:
                if org_device["status"] != "alerting":
                    del alerting_devices_file[device]
                    reference_file.remove(attrb['serial'])
                    print(f"{device} removed from alerting list..")

    print("Remove* code block complete.")
    write(REFERENCE_FiLE, reference_file)
    write(ALERTING_FiLE, alerting_devices_file)


def prepare_template_for_new_alerting_device():
    alerting_file = read(ALERTING_FiLE)
    for device in get_alerting_devices():
        if device["serial"] not in alerting_file:
            alerting_file.update({device["serial"]: {
                "name": device["name"],
                "serial": device["serial"],
                "status": device["status"],
                "added_since": datetime.now().timestamp(),
            }})
    write(ALERTING_FiLE, alerting_file)


def send_alert_for_alerting_device():
    get_device_list = ''
    alerting_file = read(ALERTING_FiLE)
    notification_template = []
    for device, attributes in alerting_file.items():
        print(attributes['name'], ((datetime.now().timestamp() - attributes["added_since"]) / 60))
        if ((datetime.now().timestamp() - attributes["added_since"]) / 60) < 1 or (
                (datetime.now().timestamp() - attributes["added_since"]) / 60) > (60 * 4):
            get_device_list = get_device_list + f"{attributes['name']}" + "\n"
            alerting_file[device].update(added_since=datetime.now().timestamp())
            notification_template.append({"name": attributes["name"], "serial": device})
    write(ALERTING_FiLE, alerting_file)

    if not notification_template:
        pass
    else:
        refrence_file = read(REFERENCE_FiLE)
        message = "<h1 style='color:black;font-weight:bold'>Alert Notifications on Meraki Dashboard</h1> <br>"
        for template in notification_template:
            if template["serial"] in refrence_file:
                message = message + f" <span style='color:gray;font-weight:bold'>Old: </span> {template['name']} with " \
                                    f"serial {template['serial']} still in alerting mode.<br> "
            else:
                message = message + f" <span style='color:red;font-weight:bold'>New: </span>{template['name']} with " \
                                    f"serial {template['serial']}  in alerting mode.<br> "
                refrence_file.append(template['serial'])
        write(REFERENCE_FiLE, refrence_file)
        TEAMS_MESSAGE = {
            "title": "Meraki Alert notifications",
            "text": message
        }
        URL = "https://capgemini.webhook.office.com/webhookb2/5b64f7f1-b046-4252-84e3-96af870f2cac@76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61/IncomingWebhook/80791143470f4f5ca1b28b0a19e9d226/97e7b15e-044e-46cb-accd-562410e8608b"
        send_message = requests.post(URL, json=TEAMS_MESSAGE)
        print(message)


while True:
    print("----------------------------------")
    print("Execution Started..")
    prepare_template_for_new_alerting_device()
    remove_alerting_devices()
    send_alert_for_alerting_device()
    print("Sleeping for 15 mins.")
    print("Execution Completed")
    print("----------------------------------")
    time.sleep(60 * 15)
    print("\n")
