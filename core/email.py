#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import config as c


def send_simple_message(target_email, subject, message):
    """send email to users"""
    return requests.post(
        "https://api.eu.mailgun.net/v3/mg.london-man.com/messages",
        auth=("api", c.MGKEY),
        data={
            "from": "Coronavirus Map <coronavirus@mg.london-man.com>",
            "to": target_email,
            "subject": subject,
            "text": message,
        },
    )
