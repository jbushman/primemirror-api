from flask import request

from pmapi.config import get_config
from pmapi.services.promote import completely_delete_rpm, delete_rpm

c = get_config()


def post_delete_rpm(data):
    try:
        del_rpm = delete_rpm(data["repo"], data["elver"], data["arch"], data["package"])
        if del_rpm:
            response = {
                "status": "success",
                "message": "RPM {} successfully deleted from {}.".format(data["package"], data["repo"])
            }
            return response, 200
        else:
            response = {
                "status": "failure",
                "message": "Failed to delete RPM {} from {}".format(data["package"], data["repo"])
            }
            return response, 409
    except Exception as e:
        response = {
            "status": "failure",
            "message": "POST delete failed.",
            "exception": str(e)
        }
        return response, 409


def get_completely_delete_rpm(rpm):
    try:
        del_rpm = completely_delete_rpm(rpm)
        if del_rpm:
            response = {
                "status": "success",
                "message": "RPM {} successfully deleted.".format(rpm)
            }
            return response, 200
        else:
            response = {
                "status": "failure",
                "message": "Failed to delete RPM {}".format(rpm)
            }
            return response, 409
    except Exception as e:
        response = {
            "status": "failure",
            "message": "POST delete failed.",
            "exception": str(e)
        }
        return response, 409
