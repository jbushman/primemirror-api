import os
import logging

from pmapi.services.sign import sign_rpm
from pmapi.services.sync import update_repo, sync_repo


def promote_rpm(init_repo, dest_repo, package, repo):
    old_rpm = init_repo + "/" + package
    new_rpm = dest_repo + "/" + package

    try:
        logging.info("Promoting {} from {} to {}".format(package, init_repo, dest_repo))
        os.system("cp "+old_rpm+" "+new_rpm)
        sign_rpm(repo, new_rpm)
        update_repo(repo)
        sync_repo(repo)
        return True
    except Exception as e:
        logging.error("Failed to promote {} from {} to {}: {}".format(package, init_repo, dest_repo, e))
        raise e
