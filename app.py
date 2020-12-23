from flask import Flask, render_template, url_for, request
import requests
import config

app = Flask(__name__)

#Add user to our email list
def subscribe_user(email, user_group_email, api_key):

    resp = requests.post(f"https://api.mailgun.net/v3/lists/{user_group_email}/members",
                         auth=("api", api_key),
                         data={"subscribed": True,
                               "address": email}
                         )

    print(resp.status_code)

    return resp
def send_email():
    return requests.post(
		"https://api.mailgun.net/v3/sandbox0ac9a4d780544304b1632775fedeee0d.mailgun.org/messages",
		auth=("api", "f08cbefc23de4f0e1243f939801c90d5-b6190e87-c113d922"),
		data={"from": "mailgun@sandbox0ac9a4d780544304b1632775fedeee0d.mailgun.org",
			"to": ["karkir0003@gmail.com"],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!?"})


@app.route("/", methods=["GET", "POST"])
def index():

    # if user submits the form
    if request.method == "POST":

        email = request.form.get('email')

        subscribe_user(email=email,
                       user_group_email="jobs_subscribers@sandbox0ac9a4d780544304b1632775fedeee0d.mailgun.org",
                       api_key=config.api_key)
    
        send_email()

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)