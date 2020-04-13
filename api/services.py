#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import Resource
import tasks
from core.database import db_session
from core import models

import core.models as m
from uuid import uuid4
import config as c
from core.helpers import get_cases_by_latlong


class RegisterUser(Resource):
    """register or if available, reactivate"""

    def put(self, email, postcode):
        # Check availability:
        existed_user = db_session.query(models.User).filter_by(email=email).first()
        if existed_user:
            if existed_user.status:
                return dict(result="ok", message="user is already active")
            existed_user.status = True
            db_session.add(existed_user)
            db_session.commit()
            taks.emailAgent.delay(
                email,
                "Coronavirus Map Account Reactivation",
                f"""
                        You requested to reactivate your notification account,
                        please click on the link bellow to reactivate your account.

                            {c.PROTOCOL}://{c.DOMAIN}:{c.PORT}/api/v1/activate/{existed_user.token}

                        If you are not requested this action, please ignore this email.

                        --
                        Be Safe.
                    """,
            )
            return dict(
                result="ok", message="User already registered. Reactivated again"
            )
        else:
            # Check postcode availabitity:
            postcode_obj = (
                db_session.query(models.Postcode).filter_by(postcode=postcode).first()
            )
            if not postcode_obj:
                return dict(result="error", message="Postcode is not valid")
            else:
                new_user = models.User(email, postcode=postcode_obj, status=True)
                db_session.add(new_user)
                db_session.commit()
                tasks.emailAgent.delay(
                    email,
                    "Welcome to Coronavirus Map Notifications",
                    f"""
                            Welcome. To complete your registeration process, please
                            click on the link bellow:

                            {c.PROTOCOL}://{c.DOMAIN}:{c.PORT}/api/v1/activate/{new_user.token}

                            If you are not requested this action, please ignore this email.

                            --
                            Be Safe.

                        """,
                )
                return dict(result="ok", message="User registered successfully")


class ActivateUser(Resource):
    """activate using token"""

    def get(self, token):
        u = db_session.query(models.User).filter_by(token=token).first()
        if not u:
            return "Token is invalid"
        else:
            u.token = uuid4().hex
            u.status = True
            db_session.add(u)
            db_session.commit()
            return "User activated"


class DeactivateUser(Resource):
    """deactivate using token"""

    def get(self, token):
        u = db_session.query(models.User).filter_by(token=token).first()
        if not u:
            return "Token is invalid"
        else:
            u.token = uuid4().hex
            u.status = False
            db_session.add(u)
            db_session.commit()
            return "User deactivated"


class GetCases(Resource):
    """ get latest case numbers """

    def get(self, lat, longt):
        result = get_cases_by_latlong(float(lat), float(longt))
        return dict(result=dict(cases=result[0], population=result[1]))
