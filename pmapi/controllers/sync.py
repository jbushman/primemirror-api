import os
import json
from flask import request

from pmapi.config import get_config
from pmapi.services.promote import sync_repo, update_repo

c = get_config()


def get_sync(repo):
    """
    Sync a primemirror repo to the mirrors infrastructure
    :param repo:
    :return:
    """
    try:
        update = update_repo(repo)
        if update:
            sync = sync_repo(repo)
            if sync:
                response = {
                    "status": "success",
                    "message": "successfully synced {} repo to mirrors".format(repo)
                }
                return response, 200
            else:
                response = {
                    "status": "failure",
                    "message": "failed to sync {} repo to mirrors".format(repo)
                }
                return response, 409
        else:
            response = {
                "status": "failure",
                "message": "failed to update {} repo".format(repo)
            }
            return response, 409
    except Exception as e:
        raise
