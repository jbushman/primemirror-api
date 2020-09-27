from pmapi.services.promote import sign_rpm
from pmapi.config import get_logger, get_repos

logger = get_logger()
repos = get_repos()


def post_sign(data):
    try:
        full_package = "{}/{}/{}/{}".format(repos[data["repo"]]["local"], data["distro"], data["arch"], data["rpm"])
        logger.info("Signing RPM {} for {}".format(data["rpm"], data["repo"]))
        sign = sign_rpm(data["repo"], full_package)
        if sign:
            logger.info("RPM {} successfully signed for {}".format(data["rpm"], data["repo"]))
            response = {
                "status": "success",
                "message": "RPM {} successfully signed for {}".format(data["rpm"], data["repo"])
            }
            return response, 200
        else:
            logger.info("Failed to sign RPM {} for {}".format(data["rpm"], data["repo"]))
            response = {
                "status": "failure",
                "message": "Failed to sign RPM {} for {}".format(data["rpm"], data["repo"])
            }
            return response, 409
    except Exception as e:
        logger.error("RPM sign failed: {}".format(e))
        response = {
            "status": "failure",
            "message": "POST sign failed.",
            "data": data,
            "exception": str(e)
        }
        return response, 409
