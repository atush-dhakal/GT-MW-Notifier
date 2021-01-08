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
    html = """\
    <html>
    <body>
    <b>Title:</b> {title}
    <br>
    <br>
    <b>Description:</b> {description}
    <br>
    <br>
    <b>Start Date:</b> {start_date}
    <br>
    <br>
    <b>End Date:</b> {end_date}
    <br>
    <br>
    <b>Contact Name:</b> {contact_name}
    <br>
    <br>
    <b>Contact Email:</b> {contact_email}
    <br>
    <br>
    <b>Hours:</b> {hours}
    <br>
    <br>
    <b>Location:</b> {location}
    <br>
    <br>
    <b>Work Study:</b> {work_study}
    <br>
    <br>
    <b>Pay Rate:</b> {pay_rate}
    <br>
    <br>
    <b>Positions Available:</b> {positions_available}
    </body>
    </html>
    """.format(title=job_detail["title"], description=job_detail["description"], start_date=job_detail["start_date"], end_date=job_detail["end_date"], contact_name=job_detail["contact_name"], contact_email=job_detail["contact_email"],
                   hours=job_detail["hours"], location=job_detail["location"], work_study=job_detail["work_study"], pay_rate=job_detail["pay_rate"], positions_available=job_detail["positions_available"])
    msg = MIMEMultipart("alternative")
    msg["Subject"] = u"Now Hiring {}".format(job_detail["title"])
    part1 = MIMEText(message,
                     "plain", "utf-8")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)

    return msg.as_string().encode('ascii')

def get_welcome_message():
    #name = "Dylan"
    message = """
    
    Thank you very much for subscribing to the GT On Campus Jobs notification service. 
    
    
    We hope this service will help you land your next on-campus job!
    
    """
    # html = """\
    # <html>
    # <body>
    # <b>Thank you very much for subscribing to the GT On Campus Jobs notification service.</b> 
    # <br>
    # <br>
    # We hope this service will help you land your next on-campus job!
    # <br>
    # <br>
    # My name is {name}
    # </body>
    # </html>
    # """.format(name=name)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = u"Welcome to the GT On Campus Jobs notification service!"
    part1 = MIMEText(message,
                     "plain", "utf-8")
    #part2 = MIMEText(html, "html")
    msg.attach(part1)
    #msg.attach(part2)

    return msg.as_string().encode('ascii')

#send welcome message for new subscribers!
def send_welcome_message(email_address):
    message = get_welcome_message()    
    send_email([email_address], message)
    
def send_notification(email_list, job_detail):
    message = get_template_message(job_detail)
    send_email(email_list, message)

def send_email(email_list, message):
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
            server.sendmail(sender_email, receiver_email, message)


def main():
    #send_notification(["gtstudentjobs@gmail.com"], {})
    send_welcome_message("karkir0003@gmail.com")
    print("success!")


if __name__ == "__main__":
    main()
