import schedule
import time
import scraper
import jobs_list
from email_notifier import send_new_job_notification
from mailchimp import OnCampusJobList


def run_schedule(database="test"):
    new_jobs = jobs_list.populate_new_jobs(database=database)

    print(f"Found {len(new_jobs)} new jobs")

    if len(new_jobs) > 0:
        custom_list = OnCampusJobList()
        members = custom_list.get_email_list()
        for job in new_jobs:
            try:
                send_new_job_notification(members, job)
            except Exception as e:
                print("Failed to send email")
                print(e)


if __name__ == "__main__":
    schedule.every(20).seconds.do(run_schedule)

    while 1:
        schedule.run_pending()
        time.sleep(1)
