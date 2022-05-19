########################################################
# .......RUN module is gathers all other modules...... #
# .....This module should be executed to start all.....#
# ....................operations...................... #
########################################################
import time
import schedule
from backend.engine.core import *


def files_version():
    # Execute the mapper and check_new_devices functions every 15 minutes.
    schedule.every(15).minutes.do(create_mapper)
    schedule.every(15).minutes.do(check_new_device)

    print(f"---------------------------------------------------------------\n"
          f"------ Welcome to Meraki SLA Calculator (Files Version) -------\n"
          f"---------------------------------------------------------------\n\n")
    ask_initial_config()
    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        # generate_network_sla_report()
        START_TIME = time.time()
        if not os.path.exists(FILES_PATH):
            create_paths()
            create_mapper()
            check_new_device()
        schedule.run_pending()
        create_folder_every_month()
        core_engine()
        copy_report_every_day()
        END_TIME = time.time()
        logger.info(f"Time taken for executing: {END_TIME - START_TIME} seconds")
        copy_report()
        logger.info(f"Sleeping for {EXECUTION_INTERVAL} seconds")
        time.sleep(EXECUTION_INTERVAL)
        print()


def db_version():
    # Execute the mapper and check_new_devices functions every 45 minutes.
    # schedule.every(5).minutes.do(create_mapper)
    # schedule.every(5).minutes.do(check_new_device)
    create_paths()
    print(f"---------------------------------------------------------------\n"
          f"------- Welcome to Meraki SLA Calculator (DB Version) ---------\n"
          f"---------------------------------------------------------------\n\n")
    ask_initial_config_for_DB()
    create_mapper_for_DB()
    check_new_device_for_DB()
    schedule.every(5).minutes.do(create_mapper_for_DB)
    schedule.every(5).minutes.do(check_new_device_for_DB)
    # Send email notifications to contacts mentioned in the gmail_notifications.py file every month.
    # schedule.every(30).days.do(send_notification)

    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        # generate_network_sla_report()
        START_TIME = time.time()
        create_paths()
        schedule.run_pending()
        create_folder_every_month()
        core_engine_for_DB()
        copy_report_every_day()
        END_TIME = time.time()
        copy_report_for_DB()
        logger.info(f"Time taken for executing: {END_TIME - START_TIME} seconds")
        logger.info(f"Sleeping for {EXECUTION_INTERVAL} seconds")
        time.sleep(EXECUTION_INTERVAL)
        print()


def start():
    print("This script has 2 version. Which version do you want to run?\n"
          f"Enter [0] to run Files version.\n"
          f"Enter [1] to run DB version")
    script_version = int(input("Enter your choice [0] or [1]: "))
    if script_version == 0:
        files_version()
    elif script_version == 1:
        db_version()
    else:
        print("Invalid input.!!!")


start()
