from scraper import JobPostingScraper, JobPostingParser
import sqlite3
from sqlite3 import Error
import pandas as pd
from datetime import datetime

# Connect to the database


def create_connection(path):
    connection = None

    # This block is a way of testing connection to the database and allows us to control what happens if there is an error
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# runs our SQL commands and outputs a DataFrame
def run_query(query, connection):
    return pd.read_sql_query(query, connection)


# build database for very first time
def write_db(connection):
    scraper = JobPostingScraper()
    job_postings = scraper.getRawJobPostings()

    jobs = [JobPostingParser(x).getJob() for x in job_postings]  # json
    titleList = []
    start_date = []
    end_date = []
    contact_name = []
    contact_email = []
    description = []
    hours = []
    location = []
    work_study = []
    pay_rate = []
    positions_available = []
    for entry in jobs:
        titleList.append(entry["title"])
        start_date.append(entry["start_date"])
        end_date.append(entry["end_date"])
        contact_name.append(entry["contact_name"])
        contact_email.append(entry["contact_email"])
        description.append(entry["description"])
        hours.append(entry["hours"])
        location.append(entry["location"])
        work_study.append(entry["work_study"])
        pay_rate.append(entry["pay_rate"])
        positions_available.append(entry["positions_available"])

    # engineer the dataframe
    job_frame = pd.DataFrame({"Job Title": titleList, "Start Date": start_date,
                              "End Date": end_date, "Contact Name": contact_name,
                              "Contact Email": contact_email, "Description": description,
                              "Hours": hours, "Location": location, "Work Study": work_study,
                              "Pay Rate": pay_rate, "Positions Available": positions_available})

    # write data frame to database file
    job_frame.to_sql('job_postings', connection,
                     if_exists='replace', index=False)


"""
Is there a new job?
"""


def newJobs(connection):
    # scrape for current data
    scraper = JobPostingScraper()
    job_postings = scraper.getRawJobPostings()

    jobs = [JobPostingParser(x).getJob() for x in job_postings]  # json

    # get prior dataframe
    currJobs = run_query('''
                        SELECT "Job Title", "Start Date", "End Date", "Description"
                        FROM job_postings;
                        ''', connection)
    descriptions_df = currJobs["Description"]  # old description

    old_description_dict = {}
    new_description_dict = {}
    for entry in descriptions_df:
        old_description_dict[entry] = 1  # replace spaces with underscores
    for job in jobs:
        new_description_dict[job["description"]] = 1

    # we only checked for description because description most unique attributes btwn two individual postings
    for k in new_description_dict.keys():
        if (k not in old_description_dict):
            return updateDataBase(connection, 1)
    return 0


def updateDataBase(connection, resultVal):
    # build most updated table and get rid of current entries
    write_db(connection)
    return resultVal


def main():
    connection = create_connection('jobs.db')  # our database
    # write_db(connection) #happen only once. NEVER RUN THIS LINE!

    print(newJobs(connection))  # check for new stuff


if __name__ == "__main__":
    main()
