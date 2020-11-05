from pmapi.config import get_logger
from pmapi.services.delete import completely_delete_rpm, delete_rpm

from flask import request

logger = get_logger()


def post_delete_rpm():
    try:
        data = request.get_json()
        logger.info("Deleting {} from {}: ".format(data["package"], data["repo"]))
        del_rpm = delete_rpm(data["repo"], data["distro"], data["arch"], data["package"])
        if del_rpm:
            logger.info("RPM {} successfully deleted from {}.".format(data["package"], data["repo"]))
            response = {
                "status": "success",
                "message": "RPM {} successfully deleted from {}.".format(data["package"], data["repo"])
            }
            return response, 200
        else:
            logger.info("Failed to delete RPM {} from {}".format(data["package"], data["repo"]))
            response = {
                "status": "failure",
                "message": "Failed to delete RPM {} from {}".format(data["package"], data["repo"])
            }
            return response, 409
    except Exception as e:
        logger.error(e)
        response = {
            "status": "failure",
            "message": "POST delete failed.",
            "exception": str(e)
        }
        return response, 409


def post_completely_delete_rpm():
    try:
        data = request.get_json()
        logger.info("Completely deleting {} from all repos".format(data["rpm"]))
        del_rpm = completely_delete_rpm(data["rpm"])
        if del_rpm:
            logger.info("RPM {} successfully deleted.".format(data["rpm"]))
            response = {
                "status": "success",
                "message": "RPM {} successfully deleted.".format(data["rpm"])
            }
            return response, 200
        else:
            logger.info("Failed to delete RPM {}".format(data["rpm"]))
            response = {
                "status": "failure",
                "message": "Failed to delete RPM {}".format(data["rpm"])
            }
            return response, 409
    except Exception as e:
        logger.error(e)
        response = {
            "status": "failure",
            "message": "POST delete failed.",
            "exception": str(e)
        }
        return response, 409
