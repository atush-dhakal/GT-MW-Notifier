import schedule
import time
import scraper
import jobs_list
from email_notifier import send_notification
from mailchimp import OnCampusJobList

def run_schedule():
    new_jobs = jobs_list.populate_new_jobs()
    print(new_jobs)
    if (len(new_jobs) > 0):
        custom_list = OnCampusJobList()
        members = custom_list.get_email_list()
        for elem in new_jobs:
            send_notification(members, elem)
    print("done!")


schedule.every(20).seconds.do(run_schedule)

while 1:
    schedule.run_pending()
    time.sleep(1)
