import os
import pexpect
import paramiko

from pmapi.config import get_config
c = get_config()


def promote_rpm(init_repo, dest_repo, package, repo):
    old_rpm = init_repo + "/" + package
    new_rpm = dest_repo + "/" + package

    try:
        if os.path.exists(new_rpm):
            os.system("cp "+old_rpm+" "+dest_repo)

        sign_rpm(repo, new_rpm)
        update_repo(dest_repo)
        sync_repo(dest_repo)
        return True
    except Exception as e:
        raise e


def sign_rpm(repo, rpm):
    try:
        if repo == "alpha":
            with open("/home/mirroradmin/.rpmmacros", "w") as f:
                f.write("% _signature gpg")
                f.write("% _gpg_path / home / mirroradmin /.gnupg")
                f.write("% _gpg_name EIG Package Management")
                f.write("% __gpg / bin / gpg1")
            child = pexpect.spawn("rpm --addsign {}".format(rpm))
            child.expect("Enter passphrase: ")
            child.sendline(c["ALPHA_PASSPHRASE"])
        elif repo == "beta":
            with open("/home/mirroradmin/.rpmmacros", "w") as f:
                f.write("% _signature gpg")
                f.write("% _gpg_path / home / mirroradmin /.gnupg")
                f.write("% _gpg_name EIG Beta Signing Authority")
                f.write("% __gpg / bin / gpg1")
            child = pexpect.spawn("rpm --addsign {}".format(rpm))
            child.expect("Enter passphrase: ")
            child.sendline(c["BETA_PASSPHRASE"])
        elif repo == "staging":
            with open("/home/mirroradmin/.rpmmacros", "w") as f:
                f.write("% _signature gpg")
                f.write("% _gpg_path / home / mirroradmin /.gnupg")
                f.write("% _gpg_name EIG Staging Signing Authority")
                f.write("% __gpg / bin / gpg1")
            child = pexpect.spawn("rpm --addsign {}".format(rpm))
            child.expect("Enter passphrase: ")
            child.sendline(c["STAGING_PASSPHRASE"])
        elif repo == "production":
            with open("/home/mirroradmin/.rpmmacros", "w") as f:
                f.write("% _signature gpg")
                f.write("% _gpg_path / home / mirroradmin /.gnupg")
                f.write("% _gpg_name EIG Production Signing Authority")
                f.write("% __gpg / bin / gpg1")
            child = pexpect.spawn("rpm --addsign {}".format(rpm))
            child.expect("Enter passphrase: ")
            child.sendline(c["PRODUCTION_PASSPHRASE"])
        return True
    except Exception as e:
        raise


def update_repo(repo):
    try:
        local = c[repo]["local"]
        stat = os.system("createrepo --update"+local)
        if stat != 0:
            raise
        return True
    except Exception as e:
        raise


def sync_repo(repo):
    try:
        rsyncopts = "-rlptgoH --delay-updates --stats"
        remotersyncopt = "-e 'ssh -i /home/mirroradmin/.ssh/id_rsa'"
        local = c[repo]["local"]
        remote = c[repo]["remote"]
        mirrors = "mirror@mirrors1.unifiedlayer.com"

        cmd = "/usr/bin/rsync --delete " + rsyncopts + " " + remotersyncopt + " " + local + " " + mirrors + ":" + remote
        stat = os.system(cmd)
        if stat != 0:
            raise

        cmd = "/bin/pushprivate " + repo
        private_key = paramiko.RSAKey.from_private_key_file(c["MIRROR_ADMIN_KEY"])
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(c["MIRRORS"], username="mirror", pkey=private_key)
        stdin, stdout, stderr = client.exec_command(cmd)
        for line in stdout:
            print("... " + line.strip("\n"))
        client.close()
        return True
    except Exception as e:
        raise
