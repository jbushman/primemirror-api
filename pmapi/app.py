#!/usr/bin/python3
from pmapi.config import Config, get_logger

import os
import logging
import requests
import connexion
from flask import Flask, request


logger = get_logger()


# if not Config.TOKEN:
#    data = {
#        "hostname": Config.HOSTNAME,
#        "ip": Config.IP,
#        "state": Config.STATE,
#        "url": Config.URL,
#        "service_type": Config.SERVICE_TYPE,
#        "roles": "'service', 'primemirror'",
#    }
#    logging.info("Registering Service: ".format(data))
#    r = requests.post("{}/register/service".format(Config.DEPLOYMENT_API_URI), json=data, verify=False)
#    resp = r.json()
#    if "TOKEN" in resp:
#        update_env("TOKEN", resp["TOKEN"])

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api("openapi.yaml", validate_responses=True, strict_validation=True)
app = flask_app.app
app.config.from_object(Config)


