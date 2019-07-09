# !/usr/bin/env python
# coding: utf-8

from flask_mail import Message
from exts import mail


def send_mail(subject, receivers, body=None, html=None):
    assert receivers
    if not body and not html:
        return False
    if isinstance(receivers, str) or isinstance(receivers, unicode):
        receivers = [receivers]
    msg = Message(subject=subject, recipients=receivers, body=body, html=html)
    try:
        mail.send(msg)
    except:
        return False
    return True
