from flask import render_template
from config import Config
from flask_mail import Message
from app import mail

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def follower_notification(followed, follower):
    send_email("[microblog] %s is now following you!" % follower.username,
               Config.ADMINS[0],
               [followed.email],
               render_template("follower_email.txt", user=followed, follower=follower),
               render_template("follower_email.html", user=followed, follower=follower))