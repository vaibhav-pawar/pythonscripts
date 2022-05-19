########################################################
# .......Starter module to prepare backend files...... #
# ..that will be used in rest of the code frequently.. #
########################################################
from datetime import timedelta

import pytz

from backend.engine.helpers import *


# Create a mapper function to map the device with the network it belongs too.
def create_mapper():
    # This function will map the devices with its network with only 2 requests.
    # 1) get org device status requests
    # 2) get networks.
    # And this function needs to executed at regular intervals to check if there are any updates in device networks.
    logger.info("creating a mapper file, will take approx a minute..")
    request_complete = False
    while not request_complete:
        try:
            mapper = {}
            create_active_network_devices_file()
            orgDevices = list(read(ORG_DEVICES))
            networks = list(read(ORG_NETWORKS_FILE))
            for device in orgDevices:
                for network in networks:
                    # If statement specific to Project Use. Should be removed for global use
                    if device["networkId"] == network["id"]:
                        mapper.update({device["serial"]: {"network": network["name"],
                                                          "networkId": network["id"],
                                                          "timeZone": network["timeZone"],
                                                          "mac": device["mac"],
                                                          "model": device["model"]}})
            write(filename=MAPPER_FILE, content=mapper)
            logger.info("Mapper file creation is completed.")
            request_complete = True
        except (ConnectionError, TypeError) as e:
            logger.exception(f"Error in creating the mapper file. Trying again")
            request_complete = False
            time.sleep(4)
            pass


# Create a mapper function to map the device with the network it belongs too.
def create_mapper_for_DB():
    # This function will map the devices with its network with only 2 requests.
    # 1) get org device status requests
    # 2) get networks.
    # And this function needs to executed at regular intervals to check if there are any updates in device networks.
    logger.info("creating a mapper file, will take approx a minute..")
    request_complete = False
    while not request_complete:
        try:
            mapper_list = []
            MAPPER_COLLECTION.create_index([("serial", ASCENDING)], unique=True)

            create_active_network_devices_file_for_DB()

            for device in DEVICES_COLLECTION.find():
                for network in NETWORKS_COLLECTION.find():
                    # If statement specific to Project Use. Should be removed for global use
                    # if network["tags"].find("0-Active") != -1:
                    if device["networkId"] == network["networkId"]:
                        try:
                            mapper = {"serial": device["serial"],
                                      "network": network["name"],
                                      "networkId": network["networkId"],
                                      "timeZone": network["timeZone"],
                                      "mac": device["mac"],
                                      "model": device["model"]}
                            mapper_list.append(json.loads(json_util.dumps(mapper)))
                            MAPPER_COLLECTION.insert_one(mapper)
                        except DuplicateKeyError:
                            MAPPER_COLLECTION.find_one_and_update({"serial": device["serial"]},
                                                                  {"$set": {"network": network["name"],
                                                                            "networkId": network["networkId"],
                                                                            "timeZone": network["timeZone"],
                                                                            "mac": device["mac"],
                                                                            "model": device["model"]}})
            logger.info("Mapper file creation is completed.")
            request_complete = True
        except (ConnectionError, TypeError) as e:
            logger.exception(f"Error in creating the mapper file. Trying again")
            request_complete = False
            time.sleep(4)
            pass


# This function will check if any new devices are added in the organisation. It will check at every execution.
# And if a new device is detected it will provide a starter json template to this device.
def check_new_device():
    """
    This function will check if any new devices are added in the organisation. It will check at every execution.
    And if a new device is detected it will provide a starter JSON template to this device.
    :return:
    """
    logger.info("checking for newly added devices (if any).")
    request_complete = False
    while not request_complete:
        try:
            check_file(SLA_JSON_FILE)
            sla_file = read(SLA_JSON_FILE)
            mapper_file = read(MAPPER_FILE)
            write(ORG_DEVICE_STATUS_FILE, get_org_devices_status_of_all_dashboard())
            for device in read(ORG_DEVICE_STATUS_FILE):
                if device["serial"] in mapper_file:
                    if device["serial"] not in read(SLA_JSON_FILE):
                        note = "Never connected to meraki" if device["lastReportedAt"] is None else "NA"
                        logger.info(f"new device detected, adding {device['name']} to sla file")
                        sla_file.update({
                            device["serial"]:
                                {"name": device["name"],
                                 "status": device["status"],
                                 "network": mapper_file[device["serial"]]["network"],
                                 "networkId": mapper_file[device["serial"]]["networkId"],
                                 "timeZone": mapper_file[device["serial"]]["timeZone"],
                                 "mac": mapper_file[device["serial"]]["mac"],
                                 "model": mapper_file[device["serial"]]["model"],
                                 "reporting_time_tracker": str(
                                     datetime.now(tz=pytz.timezone("UTC")).replace(tzinfo=None)),
                                 "last_downtime_seconds": 0,
                                 "total_downtime_seconds": 0,
                                 "note": note,
                                 "sla_start_time": str(datetime.now(tz=pytz.timezone("UTC")).replace(tzinfo=None) -
                                                       timedelta(minutes=1))}})
            write(SLA_JSON_FILE, sla_file)
            logger.info("finished checking for new devices..")
            request_complete = True
        except(ConnectionError, TypeError):

            logger.exception("Error occurred while checking new devices..")
            request_complete = False
            pass


# *****For DB****** #
# This function will check if any new devices are added in the organisation. It will check at every execution.
# And if a new device is detected it will provide a starter json template to this device.
def check_new_device_for_DB():
    """
    This function will check if any new devices are added in the organisation. It will check at every execution.
    And if a new device is detected it will provide a starter JSON template to this device.
    :return:
    """
    logger.info("checking for newly added devices (if any).")
    request_complete = False
    SLA_COLLECTION.create_index([("serial", ASCENDING)], unique=True)
    while not request_complete:
        try:
            for device in DEVICES_STATUS_COLLECTION.find():
                if device_in_mapper_already_exists(device["serial"]):
                    if SLA_COLLECTION.find_one({"serial": device["serial"]}) is None:
                        note = "Never connected to meraki" if device["lastReportedAt"] is None else "NA"
                        logger.info(f"new device detected, adding {device['name']} to SLA Database")
                        mapper_content = MAPPER_COLLECTION.find_one({"serial": device["serial"]})
                        minimal_template = {"name": device["name"],
                                            "serial": device["serial"],
                                            "status": device["status"],
                                            "network": mapper_content["network"],
                                            "networkId": mapper_content["networkId"],
                                            "timeZone": mapper_content["timeZone"],
                                            "mac": mapper_content["mac"],
                                            "model": mapper_content["model"],
                                            "reporting_time_tracker": str(
                                                datetime.now(tz=pytz.timezone("UTC")).replace(tzinfo=None)),
                                            "last_downtime_seconds": 0,
                                            "total_downtime_seconds": 0,
                                            "note": note,
                                            "sla_start_time": str(
                                                datetime.now(tz=pytz.timezone("UTC")).replace(tzinfo=None))}
                        try:
                            SLA_COLLECTION.insert_one(minimal_template)
                        except DuplicateKeyError:
                            pass
            # write(SLA_JSON_FILE, sla_file)
            logger.info("finished checking for new devices..")
            request_complete = True
        except(ConnectionError, TypeError):

            logger.exception("Error occurred while checking new devices..")
            request_complete = False
            pass
