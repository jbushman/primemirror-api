from pmapi.config import get_logger
from pmapi.services.sync import sync_directory

logger = get_logger()


def post_deploy_webui(data):
    """
    Post to deploy webui updates
    :param data:
    :return:
    """
    try:
        logger.info("Updating webui directory {} to remote {}".format(data["local"], data["remote"]))
        sync = sync_directory(data["remote"], data["local"], data["remote_host"], data["remote_user"], data["commands"])
        if sync:
            logger.info("successfully synced {} directory to {}".format(data["local"], data["remote_host"]))
            response = {
                "status": "success",
                "message": "successfully synced {} directory to {}".format(data["local"], data["remote_host"])
            }
            return response, 200
        else:
            logger.info("failed to sync {} directory to {}".format(data["local"], data["remote_host"]))
            response = {
                "status": "failure",
                "message": "failed to sync {} directory to {}".format(data["local"], data["remote_host"])
            }
            return response, 409
    except Exception as e:
        logger.error("failed to sync directory {}: {}".format(data["local"], e))
        raise e
