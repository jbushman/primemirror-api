from pmapi.config import get_logger, get_repos

import os

logger = get_logger()
repos = get_repos()


def sign_rpm(repo, package):
    try:
        logger.info("Signing {} for repo {}".format(package, repo))
        with open("/home/mirroradmin/.rpmmacros", "w") as f:
            f.write("%_signature gpg\n")
            f.write("%_gpg_path /home/mirroradmin/.gnupg\n")
            f.write("%_gpg_name {}\n".format(repos[repo]["gpg_name"]))
            f.write("%__gpg /bin/gpg1\n")
        os.system("/home/mirroradmin/rpm-sign-{}.exp {}".format(repo, package))
        return True
    except Exception as e:
        logger.error("Failed to sign {} for repo {}: {}".format(package, repo, e))
        return False
    return True
