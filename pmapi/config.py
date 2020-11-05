import os
import logging
from dotenv import load_dotenv
load_dotenv("/etc/default/pmapi")


class Config(object):
    HOSTNAME = os.getenv("HOSTNAME")
    IP = os.getenv("IP")
    STATE = os.getenv("STATE")
    ROLES = os.getenv("ROLES")
    URL = os.getenv("URL")
    SERVICE_TYPE = os.getenv("SERVICE_TYPE")
    TOKEN = os.getenv("TOKEN")
    MIRRORS = os.getenv("MIRRORS")
    MIRROR_ADMIN_KEY = os.getenv("MIRROR_ADMIN_KEY")
    ALPHA_PASSPHRASE = os.getenv("ALPHA_PASSPHRASE")
    BETA_PASSPHRASE = os.getenv("BETA_PASSPHRASE")
    STAGING_PASSPHRASE = os.getenv("STAGING_PASSPHRASE")
    PRODUCTION_PASSPHRASE = os.getenv("PRODUCTION_PASSPHRASE")
    DEPLOYMENT_SERVER_URL = os.getenv("DEPLOYMENT_SERVER_URL")


def get_logger():
    logger = logging.getLogger("bhdapi")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("/var/log/primemirror/pmapi.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def get_repos():
    results = {
        "alpha": {"local": "/var/www/html/mirrors/alpha", "remote": "/data/staging/alpha",
                  "gpg_name": "EIG Package Management"},
        "beta": {"local": "/var/www/html/mirrors/beta", "remote": "/data/staging/beta",
                 "gpg_name": "EIG Beta Signing Authority"},
        "staging": {"local": "/var/www/html/mirrors/staging", "remote": "/data/staging/staging",
                    "gpg_name": "EIG Staging Signing Authority"},
        "production": {"local": "/var/www/html/mirrors/production", "remote": "/data/staging/production",
                       "gpg_name": "EIG Production Signing Authority"}
    }
    return results
