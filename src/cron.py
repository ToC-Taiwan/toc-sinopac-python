import os
import threading
import time

import schedule


def schedule_exit():
    os._exit(0)


def add_schedule_job():
    schedule.every().day.at("08:20").do(schedule_exit)
    schedule.every().day.at("14:40").do(schedule_exit)
    while True:
        schedule.run_pending()
        time.sleep(10)


def init_schedule_job():
    threading.Thread(target=add_schedule_job, daemon=True).start()
