import logging
import pexpect

from pmapi.config import get_config

c = get_config()


def sign_rpm(repo, package):
    try:
        logging.info("Signing {} for repo {}".format(package, repo))
        if repo == "alpha":
            try:
                with open("/home/mirroradmin/.rpmmacros", "w") as f:
                    f.write("% _signature gpg\n")
                    f.write("% _gpg_path /home/mirroradmin/.gnupg\n")
                    f.write("% _gpg_name EIG Package Management\n")
                    f.write("% __gpg /bin/gpg1\n")
                child = pexpect.spawn("rpm --addsign {}".format(package))
                child.expect("Enter passphrase: ")
                child.sendline(c["ALPHA_PASSPHRASE"])
            except Exception as e:
                raise e
        elif repo == "beta":
            try:
                with open("/home/mirroradmin/.rpmmacros", "w") as f:
                    f.write("% _signature gpg\n")
                    f.write("% _gpg_path /home/mirroradmin/.gnupg\n")
                    f.write("% _gpg_name EIG Beta Signing Authority\n")
                    f.write("% __gpg /bin/gpg1\n")
                child = pexpect.spawn("rpm --addsign {}".format(package))
                child.expect("Enter passphrase: ")
                child.sendline(c["BETA_PASSPHRASE"])
            except Exception as e:
                raise e
        elif repo == "staging":
            try:
                with open("/home/mirroradmin/.rpmmacros", "w") as f:
                    f.write("% _signature gpg\n")
                    f.write("% _gpg_path /home/mirroradmin/.gnupg\n")
                    f.write("% _gpg_name EIG Staging Signing Authority\n")
                    f.write("% __gpg /bin/gpg1\n")
                child = pexpect.spawn("rpm --addsign {}".format(package))
                child.expect("Enter passphrase: ")
                child.sendline(c["STAGING_PASSPHRASE"])
            except Exception as e:
                raise e
        elif repo == "production":
            try:
                with open("/home/mirroradmin/.rpmmacros", "w") as f:
                    f.write("% _signature gpg\n")
                    f.write("% _gpg_path /home/mirroradmin/.gnupg\n")
                    f.write("% _gpg_name EIG Production Signing Authority\n")
                    f.write("% __gpg /bin/gpg1\n")
                child = pexpect.spawn("rpm --addsign {}".format(package))
                child.expect("Enter passphrase: ")
                child.sendline(c["PRODUCTION_PASSPHRASE"])
            except Exception as e:
                raise e
        return True
    except Exception as e:
        logging.error("Failed to sign {} for repo {}: {}".format(package, repo, e))
        return False
