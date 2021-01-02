import smtplib
import ssl
import sqlite3
from sqlite3 import Error
import pandas as pd


def send_notification(email_list):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "gtstudentjobs@gmail.com"
    password = input("Type your password and press enter:")
    message = """\
    Subject: Hi there

    This is a random email. If you receive, Great!"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        for elem in email_list:
            server.sendmail(sender_email, elem, message)


def main():

    print("Success!")


if __name__ == "__main__":
    main()
