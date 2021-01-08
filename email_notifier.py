import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dateutil.parser import parse
import configparser

from email_templates.new_job_info import get_new_job_email_template
from email_templates.new_subscriber import get_new_subscriber_template

config = configparser.ConfigParser()
config.read('config.ini')
google_config = config['GOOGLE']


def get_email_content(subject, template):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = u"{}".format(subject)
    msg.attach(MIMEText(template, "html", "utf-8"))

    return msg.as_string().encode('ascii')


def send_welcome_message(email_address):
    template = get_new_subscriber_template()
    subject = "Welcome to the GT On-Campus Jobs notification service!"
    email_content = get_email_content(subject, template)
    send_email([email_address], email_content)


def send_new_job_notification(email_list, job_detail):
    start_date = parse(job_detail['start_date']).strftime("%m/%d/%Y")
    end_date = parse(job_detail['end_date']).strftime("%m/%d/%Y")

    template = get_new_job_email_template(
        job_detail["title"], start_date, end_date, job_detail["pay_rate"],
        job_detail["work_study"], job_detail["positions_available"],
        job_detail["location"], job_detail["hours"], job_detail["description"],
        job_detail["contact_name"], job_detail["contact_email"])

    subject = "GT On-Campus Jobs | Now Hiring {}".format(job_detail["title"])
    email_content = get_email_content(subject, template)
    send_email(email_list, email_content)


def send_email(email_list, email_content):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"

    sender_email = "gtstudentjobs@gmail.com"
    password = google_config['EMAIL_PASSWORD']

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        for receiver_email in email_list:
            server.sendmail(sender_email, receiver_email, email_content)


def main():
    # import database
    # db = database.JobPostingDatabase()
    # test_job = db.get_all_job_postings()[0]

    # send_new_job_notification(["gtstudentjobs@gmail.com"], test_job)

    send_welcome_message("sebop97458@nonicamy.com")


if __name__ == "__main__":
    main()
