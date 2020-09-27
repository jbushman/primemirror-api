from pmapi.services.sign import sign_rpm
from pmapi.services.sync import update_repo, sync_repo
from pmapi.config import get_logger

import os

logger = get_logger()


def promote_rpm(init_repo, dest_repo, package, repo, distro):
    old_rpm = "{}/{}".format(init_repo, package)
    new_rpm = "{}/{}".format(dest_repo, package)

    try:
        logger.info("Promoting {} from {} to {}".format(package, init_repo, dest_repo))
        os.system("cp {} {}".format(old_rpm, new_rpm))
        sign_rpm(repo, new_rpm)
        update_repo(repo, distro)
        sync_repo(repo)
        return True
    except Exception as e:
        logger.error("Failed to promote {} from {} to {}: {}".format(package, init_repo, dest_repo, e))
        raise e
