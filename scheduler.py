import schedule
import time
import scraper
import jobs_list


def run_schedule():
    jobs_list.populate_new_jobs()
    print("done!")


schedule.every(20).seconds.do(run_schedule)

while 1:
    schedule.run_pending()
    time.sleep(1)
