from flask import Flask, render_template, request, jsonify
import util

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/subscribe", methods=["POST"])
def add_subscriber():
    email_subscriber = request.form['email']
    recaptcha_response = request.form['g-recaptcha-response']

    # Make sure the email provided is valid
    if not util.is_valid_email(email_subscriber):
        return {'error': 'Please enter a valid email address'}, 400

    # Verify the recaptcha token. Helps to prevent spam and automated bots submissions
    if not util.is_valid_recaptcha(recaptcha_response):
        return {'error': 'Failed to validate the reCAPTCHA'}, 400

    try:
        util.add_email_subscriber(email_subscriber)
        return {'success': True}, 200
    except Exception as e:
        print(e)
        return {'error': "Failed to add subscriber"}, 500


if __name__ == '__main__':
    app.run(debug=True)
