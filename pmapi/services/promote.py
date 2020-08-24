import os
import glob
import pexpect
import paramiko

from pmapi.config import get_config
c = get_config()


def completely_delete_rpm(package):
    """
    Wipe an RPM from all repos and mirrors
    :param package:
    :return: True
    """
    try:
        rpms = glob.glob('/var/www/html/mirrors/*/*/*/'+package, recursive=True)
        for rpm in rpms:
            try:
                os.remove(rpm)
            except:
                raise Exception("Error while deleting "+rpm)
        return True
    except Exception as e:
        raise e


def delete_rpm(repo, elver, arch, package):
    try:
        full_package = c[repo]["local"] + "/" + "centos" + str(elver) + "/" + arch + "/" + package
        os.remove(full_package)
        update_repo(repo)
        sync_repo(repo)
        return True
    except:
        raise "Error while deleting "+full_package


def promote_rpm(init_repo, dest_repo, package, repo):
    old_rpm = init_repo + "/" + package
    new_rpm = dest_repo + "/" + package

    try:
        os.system("cp "+old_rpm+" "+new_rpm)
        sign_rpm(repo, new_rpm)
        update_repo(repo)
        sync_repo(repo)
        return True
    except Exception as e:
        raise e


def sign_rpm(repo, rpm):
    try:
        if repo == "alpha":
            with open("/home/mirroradmin/.rpmmacros", "w") as f:
                f.write("% _signature gpg\n")
                f.write("% _gpg_path /home/mirroradmin/.gnupg\n")
                f.write("% _gpg_name EIG Package Management\n")
                f.write("% __gpg /bin/gpg1\n")
            child = pexpect.spawn("rpm --addsign {}".format(rpm))
            child.expect("Enter passphrase: ")
            child.sendline(c["ALPHA_PASSPHRASE"])
        elif repo == "beta":
            with open("/home/mirroradmin/.rpmmacros", "w") as f:
                f.write("% _signature gpg\n")
                f.write("% _gpg_path /home/mirroradmin/.gnupg\n")
                f.write("% _gpg_name EIG Beta Signing Authority\n")
                f.write("% __gpg /bin/gpg1\n")
            child = pexpect.spawn("rpm --addsign {}".format(rpm))
            child.expect("Enter passphrase: ")
            child.sendline(c["BETA_PASSPHRASE"])
        elif repo == "staging":
            with open("/home/mirroradmin/.rpmmacros", "w") as f:
                f.write("% _signature gpg\n")
                f.write("% _gpg_path /home/mirroradmin/.gnupg\n")
                f.write("% _gpg_name EIG Staging Signing Authority\n")
                f.write("% __gpg /bin/gpg1\n")
            child = pexpect.spawn("rpm --addsign {}".format(rpm))
            child.expect("Enter passphrase: ")
            child.sendline(c["STAGING_PASSPHRASE"])
        elif repo == "production":
            with open("/home/mirroradmin/.rpmmacros", "w") as f:
                f.write("% _signature gpg\n")
                f.write("% _gpg_path /home/mirroradmin/.gnupg\n")
                f.write("% _gpg_name EIG Production Signing Authority\n")
                f.write("% __gpg /bin/gpg1\n")
            child = pexpect.spawn("rpm --addsign {}".format(rpm))
            child.expect("Enter passphrase: ")
            child.sendline(c["PRODUCTION_PASSPHRASE"])
        return True
    except Exception as e:
        raise e


def update_repo(repo):
    try:
        local = c[repo]["local"]
        stat = os.system("createrepo --update "+local)
        if stat != 0:
            raise
        return True
    except Exception as e:
        raise e


def sync_repo(repo):
    try:
        rsyncopts = " -rlptgoH --delay-updates --stats "
        remotersyncopt = " -e 'ssh -i /home/mirroradmin/.ssh/id_rsa' "
        local = c[repo]["local"]
        remote = c[repo]["remote"]
        mirrors = " mirror@mirrors1.unifiedlayer.com:"

        cmd = "/usr/bin/rsync --delete" + rsyncopts + remotersyncopt + local + mirrors + remote
        stat = os.system(cmd)
        if stat != 0:
            raise Exception("Error with rsync.")

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
        raise e
