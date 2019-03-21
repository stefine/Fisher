#!/usr/bin/python
# -*- coding:utf-8 -*-
from threading import Thread

from flask_mail import Message
from flask import current_app, render_template, app
from app import mail


def send_asynic_mail(app, msg):
    with app.app_context():
        try:
            mail.send()
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    msg = Message('[鱼书]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    g_app = current_app._get_current_object()
    t = Thread(target=send_asynic_mail, args=[g_app, msg])
    t.start()
    mail.send_messages(msg)
