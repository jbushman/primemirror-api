import os
from dotenv import load_dotenv
load_dotenv("/etc/default/pmapi")


def get_config():
    results = {}
    results["alpha"] = {"local": "/var/www/html/mirrors/alpha/", "remote": "/data/staging/alpha/"}
    results["beta"] = {"local": "/var/www/html/mirrors/beta/", "remote": "/data/staging/beta/"}
    results["staging"] = {"local": "/var/www/html/mirrors/staging/", "remote": "/data/staging/staging/"}
    results["production"] = {"local": "/var/www/html/mirrors/production/", "remote": "/data/staging/production/"}
    results["HOSTNAME"] = os.getenv("HOSTNAME")
    results["IP"] = os.getenv("IP")
    results["STATE"] = os.getenv("STATE")
    results["ROLES"] = os.getenv("ROLES")
    results["URL"] = os.getenv("URL")
    results["SERVICE_TYPE"] = os.getenv("SERVICE_TYPE")
    results["TOKEN"] = os.getenv("TOKEN")
    results["MIRRORS"] = os.getenv("MIRRORS")
    results["MIRROR_ADMIN_KEY"] = os.getenv("MIRROR_ADMIN_KEY")
    results["ALPHA_PASSPHRASE"] = os.getenv("ALPHA_PASSPHRASE")
    results["BETA_PASSPHRASE"] = os.getenv("BETA_PASSPHRASE")
    results["STAGING_PASSPHRASE"] = os.getenv("STAGING_PASSPHRASE")
    results["PRODUCTION_PASSPHRASE"] = os.getenv("PRODUCTION_PASSPHRASE")
    results["DEPLOYMENT_SERVER_URL"] = os.getenv("DEPLOYMENT_SERVER_URL")
    return results