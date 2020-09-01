import os
import paramiko
import logging

from pmapi.config import get_config
c = get_config()


def update_repo(repo):
    try:
        logging.info("Updating metadata for {}".format(repo))
        local = c[repo]["local"]
        stat = os.system("createrepo --update "+local)
        if stat != 0:
            raise
        return True
    except Exception as e:
        logging.error("Failed to update metadata for {} repo: {}".format(repo, e))
        raise e


def sync_repo(repo):
    try:
        logging.info("syncing repo {}".format(repo))
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
        logging.error("Failed to sync repo {}: {}".format(repo, e))
        raise e


def sync_directory(remote, local, remote_host, remote_user, commands=None):
    try:
        logging.info("syncing directory {} to {}".format(local, remote))
        rsyncopts = "-rlptgoH --delay-updates --stats"
        remotersyncopt = "-e 'ssh -i /home/mirroradmin/.ssh/id_rsa'"

        cmd = "/usr/bin/rsync --delete {} {} {} {}@{} {}".format(rsyncopts, remotersyncopt, local, remote_user,
                                                                 remote_host, remote)
        stat = os.system(cmd)
        if stat != 0:
            raise Exception("Error with rsync.")

        if commands:
            private_key = paramiko.RSAKey.from_private_key_file(c["MIRROR_ADMIN_KEY"])
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.connect(remote_host, username=remote_user, pkey=private_key)
            for cmd in commands:
                stdin, stdout, stderr = client.exec_command(cmd)
                for line in stdout:
                    print("... " + line.strip("\n"))
            client.close()
        return True
    except Exception as e:
        logging.error("Failed to sync directory {}: {}".format(local, e))
        raise e
