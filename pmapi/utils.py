import os
import sys
from collections import OrderedDict
from subprocess import check_call, Popen


class LastUpdated(OrderedDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


def install_pkgs(packages):
    packages = [x.encode('utf-8') for x in packages]
    packages = ' '.join(packages)
    check_call("sudo yum clean all", verbose=False)
    stat = check_call("sudo yum -y install {}".format(packages), verbose=False)
    if stat != 0:
        raise Exception(stat)


def restart_service(service):
    restart = "systemctl restart {}".format(service)
    Popen([sys.executable, restart])


def update_env(key, value):
    os.environ[key] = value
    env = LastUpdated()
    with open(".env") as f:
        for line in f:
            (k, v) = line.split("=")
            env[k] = v
    env[key] = value

    with open(".env", "w") as f:
        for k in env.keys():
            line = "{}={}\n".format(k, env[k])
            f.write(line)