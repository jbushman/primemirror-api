from pmapi.config import get_logger, get_repos
from pmapi.services.promote import promote_rpm

logger = get_logger()
repos = get_repos()


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
        logger.info("Promoting: {} from {} repo to {} repo".format(data["package"], data["init_repo"],
                                                                   data["dest_repo"]))
        init_repo = "{}/{}/{}".format(repos[data["init_repo"]]["local"], data["distro"], data["arch"])
        dest_repo = "{}/{}/{}".format(repos[data["dest_repo"]]["local"], data["distro"], data["arch"])
        result = promote_rpm(init_repo, dest_repo, data["package"], data["dest_repo"], data["distro"])
        if result:
            logger.info("{} has been promoted to {}".format(data["package"], data["dest_repo"]))
            response = {
                "status": "success",
                "message": "Package has been promoted."
            }
            return response, 200
        else:
            logger.info("Failed to promote {} to {}".format(data["package"], data["dest_repo"]))
            response = {
                "status": "failure",
                "message": "failed to promote {} to {}".format(data["package"], data["dest_repo"])
            }
            return response, 409

    except Exception as e:
        logger.error("Package promotion failed: {}".format(e))
        response = {
            "status": "failure",
            "message": "Package promotion failed.",
            "exception": str(e)
        }
        return response, 409

