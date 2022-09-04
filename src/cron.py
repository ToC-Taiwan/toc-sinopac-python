import os
import threading
import time

import schedule


def add_schedule_job():
    schedule.every().day.at("01:20").do(os._exit, 0)
    schedule.every().day.at("08:20").do(os._exit, 0)
    schedule.every().day.at("14:40").do(os._exit, 0)
    while True:
        schedule.run_pending()
        time.sleep(10)


def init_schedule_job():
    threading.Thread(target=add_schedule_job).start()
