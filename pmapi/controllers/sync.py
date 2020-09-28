from pmapi.config import get_logger
from pmapi.services.sync import sync_repo, update_repo

from flask import request

logger = get_logger()


def post_sync_repo():
    """
    Sync a primemirror repo to the mirrors infrastructure
    :param repo: alpha, beta, staging or production
    :param distro: centos7 or fedora32
    :return:
    """
    try:
        data = request.get_json()
        logger.info("Updating metadata for {}".format(data["repo"]))
        update = update_repo(data["repo"], data["distro"])
        if update:
            sync = sync_repo(data["repo"])
            if sync:
                logger.info("successfully synced {} repo to mirrors".format(data["repo"]))
                response = {
                    "status": "success",
                    "message": "successfully synced {} repo to mirrors".format(data["repo"])
                }
                return response, 200
            else:
                logger.info("failed to sync {} repo to mirrors".format(data["repo"]))
                response = {
                    "status": "failure",
                    "message": "failed to sync {} repo to mirrors".format(data["repo"])
                }
                return response, 409
        else:
            logger.info("failed to update {} repo".format(data["repo"]))
            response = {
                "status": "failure",
                "message": "failed to update {} repo".format(data["repo"])
            }
            return response, 409
    except Exception as e:
        logger.error("failed to sync repo {}: {}".format(data["repo"], e))
        raise
