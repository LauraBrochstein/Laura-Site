from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_wtf.recaptcha import RecaptchaField
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__, static_url_path="")
Bootstrap(app)

import os
SECRET_APP_KEY = os.urandom(32)
SITE_KEY = os.environ.get("SITE_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_PUBLIC_KEY = SITE_KEY,
    RECAPTCHA_PRIVATE_KEY = SECRET_KEY
))
app.config['SECRET_KEY'] = SECRET_APP_KEY

class ContactForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()], render_kw={"placeholder": "First Name"})
    lastname = StringField("Last Name", validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
    email = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder": "Email"})
    message = TextAreaField("Message", validators=[DataRequired()], render_kw={"placeholder": "Message"})
    recaptcha = RecaptchaField()
    submit = SubmitField("Send")

from urllib.parse import urlparse, urlunparse

def send_email(receiver, subject, message):
    messagehtml = MIMEMultipart()
    messagehtml["To"] = receiver
    messagehtml["From"] = 'eitantravels25@gmail.com'
    messagehtml["Subject"] = subject

    title = subject
    messageText = MIMEText(message,'html')
    messagehtml.attach(messageText)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("eitantravels25@gmail.com", "msoiknaautelynsv")
    s.sendmail("eitantravels25@gmail.com", receiver, messagehtml.as_string())
    s.quit()

@app.before_request
def redirect_nonwww():
    """Redirect non-www requests to www."""
    urlparts = urlparse(request.url)
    if urlparts.netloc == 'laurashulmanbrochstein.org':
        urlparts_list = list(urlparts)
        urlparts_list[1] = 'www.laurashulmanbrochstein.org'
        return redirect(urlunparse(urlparts_list), code=301)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/resources")
def resources():
    return render_template("resources.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    contactform = ContactForm()
    if contactform.validate_on_submit():
       try:
            firstname = str(contactform.firstname.data)
            lastname = str(contactform.lastname.data)
            email = str(contactform.email.data)
            message = str(contactform.message.data)
            # create mail object
            send_email("laura.brochstein@gmail.com", f"New Contact Message from {firstname} {lastname} at {email}:", f"Hi Laura!<br>We got new contact information from {firstname} {lastname}, their email is {email},<br>Their Message:\n{message}")
            return render_template("sent.html")
       except Exception as err:
           return jsonify({"Error": str(err)})
    return render_template("contact.html", form=contactform)


@app.route("/services/managing-life-transitions")
def managing_life_transitions():
    return render_template("lifetransitions.html")

@app.route("/services/parenting")
def parenting():
    return render_template("parenting.html")

@app.route("/services/lgbtq-identity")
def lgbtq():
    return render_template("lgbtq.html")

@app.route("/services/anxiety-depression")
def anxiety():
    return render_template("anxiety.html")

@app.errorhandler(404)
def errorpage(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")