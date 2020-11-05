import os
import glob

from pmapi.config import get_logger, get_repos
from pmapi.services.sync import update_repo, sync_repo

logger = get_logger()
repos = get_repos()


def completely_delete_rpm(package):
    """
    Wipe an RPM from all repos and mirrors
    :param package:
    :return: True
    """
    try:
        logger.info("completely deleting {} from all repo".format(package))
        rpms = glob.glob("/var/www/html/mirrors/*/*/*/{}".format(package), recursive=True)
        for rpm in rpms:
            try:
                os.remove(rpm)
            except:
                raise Exception("Error while deleting "+rpm)
        return True
    except Exception as e:
        logger.error("Failed to delete rpm {}: {}".format(rpm, e))
        raise e


def delete_rpm(repo, distro, arch, package):
    try:
        full_package = "{}/{}/{}/{}".format(repos[repo]["local"], distro, arch, package)
        os.remove(full_package)
        update_repo(repo)
        sync_repo(repo)
        return True
    except Exception as e:
        logger.error("Error while deleting {}: {} ".format(full_package, e))
        raise "Error while deleting {}: {} ".format(full_package, e)
