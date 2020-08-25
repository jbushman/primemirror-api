import os
import glob
import logging

from pmapi.config import get_config
from pmapi.services.sync import update_repo, sync_repo

c = get_config()


def completely_delete_rpm(package):
    """
    Wipe an RPM from all repos and mirrors
    :param package:
    :return: True
    """
    try:
        logging.info("completely deleting {} from all repo".format(package))
        rpms = glob.glob('/var/www/html/mirrors/*/*/*/'+package, recursive=True)
        for rpm in rpms:
            try:
                os.remove(rpm)
            except:
                raise Exception("Error while deleting "+rpm)
        return True
    except Exception as e:
        logging.error("Failed to delete rpm {}: {}".format(rpm, e))
        raise e


def delete_rpm(repo, elver, arch, package):
    try:
        full_package = c[repo]["local"] + "/" + "centos" + str(elver) + "/" + arch + "/" + package
        os.remove(full_package)
        update_repo(repo)
        sync_repo(repo)
        return True
    except Exception as e:
        logging.error("Error while deleting {}: {} ".format(full_package, e))
        raise "Error while deleting {}: {} ".format(full_package, e)
