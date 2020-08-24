import os
import requests
from flask import request

from pmapi.config import get_config
from pmapi.services.promote import sign_rpm

c = get_config()


def post_sign(data):
    try:
        sign = sign_rpm(data["repo"], data["rpm"])
        if sign:
            response = {
                "status": "success",
                "message": "RPM {} successfully signed for {}".format(data["rpm"], data["repo"])
            }
            return response, 200
        else:
            response = {
                "status": "failure",
                "message": "Failed to sign RPM {} for {}".format(data["rpm"], data["repo"])
            }
            return response, 409
    except Exception as e:
        response = {
            "status": "failure",
            "message": "POST sign failed.",
            "exception": str(e)
        }
        return response, 409
