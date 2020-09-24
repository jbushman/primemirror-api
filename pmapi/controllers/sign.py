import logging

from pmapi.config import get_config
from pmapi.services.promote import sign_rpm

c = get_config()


def post_sign(data):
    try:
        package = c[data["repo"]]["local"] + str(data["distro"]) + "/" + data["arch"] + "/" + data["rpm"]
        logging.info("Signing RPM {} for {}".format(data["rpm"], data["repo"]))
        sign = sign_rpm(data["repo"], package)
        if sign:
            logging.info("RPM {} successfully signed for {}".format(data["rpm"], data["repo"]))
            response = {
                "status": "success",
                "message": "RPM {} successfully signed for {}".format(data["rpm"], data["repo"])
            }
            return response, 200
        else:
            logging.info("Failed to sign RPM {} for {}".format(data["rpm"], data["repo"]))
            response = {
                "status": "failure",
                "message": "Failed to sign RPM {} for {}".format(data["rpm"], data["repo"])
            }
            return response, 409
    except Exception as e:
        logging.error("RPM sign failed: {}".format(e))
        response = {
            "status": "failure",
            "message": "POST sign failed.",
            "data": data,
            "exception": str(e)
        }
        return response, 409
