import smtplib
import ssl
import sqlite3
from sqlite3 import Error
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
google_config = config['GOOGLE']


def get_template_message(job_detail):
    message = """\
    
    Title: {}
    Description: {}
    Start Date: {}
    End Date: {}
    Contact Name: {}
    Contact Email: {}
    Hours: {}
    Location: {}
    Work Study: {}
    Pay Rate: {}
    Positions Available: {}
        """.format(job_detail["title"], job_detail["description"], job_detail["start_date"], job_detail["end_date"], job_detail["contact_name"], job_detail["contact_email"],
                   job_detail["hours"], job_detail["location"], job_detail["work_study"], job_detail["pay_rate"], job_detail["positions_available"])
    msg = MIMEMultipart("alternative")
    msg["Subject"] = u"Now Hiring {}".format(job_detail["title"])
    part1 = MIMEText(message,
                     "plain", "utf-8")
    msg.attach(part1)

    return msg.as_string().encode('ascii')

def get_welcome_message():
    message = """\
    
    Thank you very much for subscribing to the GT On Campus Jobs notification service. 
    We hope this service will help you land your next on-campus job!
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = u"Welcome to the GT On Campus Jobs notification service!"
    part1 = MIMEText(message,
                     "plain", "utf-8")
    msg.attach(part1)

    return msg.as_string().encode('ascii')

#send welcome message for new subscribers!
def send_welcome_message(email_address):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"

    sender_email = "gtstudentjobs@gmail.com"
    password = google_config['EMAIL_PASSWORD']

    message = get_welcome_message()

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, email_address, message)
    
def send_notification(email_list, job_detail):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"

    sender_email = "gtstudentjobs@gmail.com"
    password = google_config['EMAIL_PASSWORD']

    message = get_template_message(job_detail)

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        for elem in email_list:
            server.sendmail(sender_email, elem, message)


def main():
    send_notification(["gtstudentjobs@gmail.com"], {})
    print("success!")


if __name__ == "__main__":
    main()
