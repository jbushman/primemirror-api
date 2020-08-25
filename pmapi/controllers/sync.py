import logging

from pmapi.config import get_config
from pmapi.services.sync import sync_repo, update_repo

c = get_config()


def get_sync(repo):
    """
    Sync a primemirror repo to the mirrors infrastructure
    :param repo:
    :return:
    """
    try:
        logging.info("Updating metadata for {}".format(repo))
        update = update_repo(repo)
        if update:
            sync = sync_repo(repo)
            if sync:
                logging.info("successfully synced {} repo to mirrors".format(repo))
                response = {
                    "status": "success",
                    "message": "successfully synced {} repo to mirrors".format(repo)
                }
                return response, 200
            else:
                logging.info("failed to sync {} repo to mirrors".format(repo))
                response = {
                    "status": "failure",
                    "message": "failed to sync {} repo to mirrors".format(repo)
                }
                return response, 409
        else:
            logging.info("failed to update {} repo".format(repo))
            response = {
                "status": "failure",
                "message": "failed to update {} repo".format(repo)
            }
            return response, 409
    except Exception as e:
        logging.error("failed to sync repo {}: {}".format(repo, e))
        raise
