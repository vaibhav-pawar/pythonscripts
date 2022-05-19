from pymongo import *
from pymongo.errors import *
from bson import json_util, ObjectId

client = MongoClient("localhost", 27017)
MERAKI_AVAILABILITY_DB = client["meraki_availability"]
NETWORKS_COLLECTION = MERAKI_AVAILABILITY_DB['org_networks']
DEVICES_COLLECTION = MERAKI_AVAILABILITY_DB['org_devices']
MAPPER_COLLECTION = MERAKI_AVAILABILITY_DB['mapper']
SLA_COLLECTION = MERAKI_AVAILABILITY_DB['devices_sla']
DEVICES_STATUS_COLLECTION = MERAKI_AVAILABILITY_DB['org_devices_status']
BACKUP_SLA_COLLECTION = MERAKI_AVAILABILITY_DB["sla_collections_backup"]
ORG_CONFIG_COLLECTION = MERAKI_AVAILABILITY_DB["organisations_config"]
NETWORK_MAINTENANCE_COLLECTION = MERAKI_AVAILABILITY_DB['org_network_maintenance']
DEVICE_MAINTENANCE_COLLECTION = MERAKI_AVAILABILITY_DB['org_device_maintenance']
