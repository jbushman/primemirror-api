from pmapi.config import get_logger
from pmapi.services.sync import sync_repo, update_repo

logger = get_logger()


def get_sync(repo, distro):
    """
    Sync a primemirror repo to the mirrors infrastructure
    :param repo: alpha, beta, staging or production
    :param distro: centos7 or fedora32
    :return:
    """
    try:
        logger.info("Updating metadata for {}".format(repo))
        update = update_repo(repo, distro)
        if update:
            sync = sync_repo(repo)
            if sync:
                logger.info("successfully synced {} repo to mirrors".format(repo))
                response = {
                    "status": "success",
                    "message": "successfully synced {} repo to mirrors".format(repo)
                }
                return response, 200
            else:
                logger.info("failed to sync {} repo to mirrors".format(repo))
                response = {
                    "status": "failure",
                    "message": "failed to sync {} repo to mirrors".format(repo)
                }
                return response, 409
        else:
            logger.info("failed to update {} repo".format(repo))
            response = {
                "status": "failure",
                "message": "failed to update {} repo".format(repo)
            }
            return response, 409
    except Exception as e:
        logging.error("failed to sync repo {}: {}".format(repo, e))
        raise
