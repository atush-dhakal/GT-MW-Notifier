import sqlite3
import pandas as pd
from scraper import JobPostingScraper, JobPostingParser
from database import Database


DATABASE_COLUMNS = ["job_title", "start_date", "end_date", "contact_name", "contact_email",
                    "description", "hours", "location", "work_study", "pay_rate", "positions_available"]

# Populate the database with default values for the first time


def seed_database():
    scraper = JobPostingScraper()
    job_postings = scraper.getRawJobPostings()

    jobs = [JobPostingParser(x).getJob() for x in job_postings]

    """
        Jobs has a list of dictionary for a given job posting
        If an attribute is missing, it will be set to None
        So we can directly get the values from the dictionary to build our data frame
    """
    job_frame = pd.DataFrame([list(x.values())
                              for x in jobs], columns=DATABASE_COLUMNS)

    db = Database(path="jobs.db")
    db.write_to_database(job_frame, table_name='job_postings')


"""
Is there a new job?
"""


def populate_new_jobs():
    db = Database(path="jobs.db")

    # scrape for current data
    scraper = JobPostingScraper()
    job_postings = scraper.getRawJobPostings()

    jobs = [JobPostingParser(x).getJob() for x in job_postings]
    new_jobs = []

    for job in jobs:
        current_job_posting = list(job.values())
        current_job_frame = pd.DataFrame(
            [current_job_posting], columns=DATABASE_COLUMNS)

        try:

            db.write_to_database(current_job_frame, table_name="job_postings")
            new_jobs.append(job)
        # Because of unique index, duplicate jobs will throw IntegrityError
        except sqlite3.IntegrityError as e:
            # Found a duplicate job, ignore this job
            continue
        except sqlite3.Error as e:
            print(e)

    return new_jobs


def main():
    # seed_database()  # happen only once. NEVER RUN THIS LINE!
    new_jobs = populate_new_jobs()
    print(new_jobs)


if __name__ == "__main__":
    main()
