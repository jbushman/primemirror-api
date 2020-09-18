import logging
import pexpect
import os

from pmapi.config import get_config

c = get_config()

repo_cfg = {
    'alpha': {
        'gpg_name':     'EIG Package Management',
        'passphrase':   'ALPHA_PASSPHRASE'
        },
    'beta': {
        'gpg_name':     'EIG Beta Signing Authority',
        'passphrase':   'BETA_PASSPHRASE'
        },
    'staging': {
        'gpg_name':     'EIG Staging Signing Authority',
        'passphrase':   'STAGING_PASSPHRASE'
        },
    'production': {
        'gpg_name':     'EIG Production Signing Authority',
        'passphrase':   'PRODUCTION_PASSPHRASE'
        }
}

def sign_rpm(repo, package):
    try:
        logging.info("Signing {} for repo {}".format(package, repo))
        with open("/home/mirroradmin/.rpmmacros", "w") as f:
            f.write("%_signature gpg\n")
            f.write("%_gpg_path /home/mirroradmin/.gnupg\n")
            f.write("%_gpg_name {}\n".format(repo_cfg[repo]['gpg_name']))
            f.write("%__gpg /bin/gpg1\n")
        os.system("/home/mirroradmin/rpm-sign-alpha.exp {}".format(package))
    except Exception as e:
        logging.error("Failed to sign {} for repo {}: {}".format(package, repo, e))
        return False
