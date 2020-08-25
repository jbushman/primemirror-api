import logging

from pmapi.config import get_config
from pmapi.services.promote import promote_rpm

c = get_config()


def post_promote(data):
    """
    Promote packages from one repository to another
    Sign packages for the promoted repo
    Copy package to promoted repo
    Update repodata
    Sync repo to mirrors infrastructure
    :return:
    """
    try:
        logging.info("Promoting: {} from {} repo to {} repo".format(data["package"], data["init_repo"],
                                                                    data["dest_repo"]))
        init_repo = c[data["init_repo"]]["local"] + "centos" + str(data["elver"]) + "/" + data["arch"]
        dest_repo = c[data["dest_repo"]]["local"] + "centos" + str(data["elver"]) + "/" + data["arch"]

        result = promote_rpm(init_repo, dest_repo, data["package"], data["dest_repo"])
        if result:
            logging.info("{} has been promoted to {}".format(data["package"], data["dest_repo"]))
            response = {
                "status": "success",
                "message": "Package has been promoted."
            }
            return response, 200
        else:
            logging.info("Failed to promote {} to {}".format(data["package"], data["dest_repo"]))
            response = {
                "status": "failure",
                "message": "failed to promote {} to {}".format(data["package"], data["dest_repo"])
            }
            return response, 409

    except Exception as e:
        logging.error("Package promotion failed: {}".format(e))
        response = {
            "status": "failure",
            "message": "Package promotion failed.",
            "exception": str(e)
        }
        return response, 409

