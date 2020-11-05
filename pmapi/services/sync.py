from pmapi.config import Config, get_logger, get_repos

import os
import paramiko

logger = get_logger()
repos = get_repos()


def update_repo(repo, distro):
    try:
        full_repo = "{}/{}".format(repo, distro)
        logger.info("Updating metadata for {}".format(full_repo))
        stat = os.system("createrepo --update {}".format(full_repo))
        if stat != 0:
            raise Exception("Error with createrepo")
        return True
    except Exception as e:
        logger.error("Failed to update metadata for {} repo: {}".format(full_repo, e))
        raise e


def sync_repo(repo, distro):
    try:
        full_repo = "{}/{}".format(repo, distro)
        logger.info("syncing repo {}".format(full_repo))
        rsyncopts = "-rlptgoH --delay-updates --stats"
        remotersyncopts = "-e 'ssh -i /home/mirroradmin/.ssh/id_rsa'"
        local_dir = "{}/{}".format(repos[repo]["local"], distro)
        remote_dir = "{}/{}".format(repos[repo]["remote"], distro)
        mirrors = " mirror@mirrors1.unifiedlayer.com:"

        cmd = f"/usr/bin/rsync --delete {rsyncopts} {remotersyncopts} {local_dir} {mirrors} {remote_dir}"
        stat = os.system(cmd)
        if stat != 0:
            raise Exception("Error with rsync.")

        cmd = "/bin/pushprivate {}".format(repo)
        private_key = paramiko.RSAKey.from_private_key_file(Config.MIRROR_ADMIN_KEY)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(Config.MIRRORS, username="mirror", pkey=private_key)
        stdin, stdout, stderr = client.exec_command(cmd)
        for line in stdout:
            print("... " + line.strip("\n"))
        client.close()
        return True
    except Exception as e:
        logger.error("Failed to sync repo {}: {}".format(repo, e))
        raise e


def sync_directory(remote_dir, local_dir, remote_host, remote_user, commands=None):
    try:
        logger.info("syncing directory {} to {}".format(local_dir, remote_dir))
        rsyncopts = "--delete -rlptgoH --delay-updates --stats"
        remotersyncopt = "-e 'ssh -i /home/jenkins/.ssh/id_rsa'"

        cmd = "/usr/bin/rsync {} {} {} {}@{}:{}".format(rsyncopts, remotersyncopt, local_dir, remote_user, remote_host,
                                                        remote_dir)
        logger.info(cmd)
        stat = os.system(cmd)
        if stat != 0:
            raise Exception("Error with rsync.")

        if commands:
            private_key = paramiko.RSAKey.from_private_key_file(Config.MIRROR_ADMIN_KEY)
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
        logger.error("Failed to sync directory {}: {}".format(local_dir, e))
        raise e
