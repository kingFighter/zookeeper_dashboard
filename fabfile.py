from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.files import exists
from hostsetting import *
import os

env.hosts.append(host)
env.password = password

confPath = 'zoo.cfg'
myidPath = 'myid'
local('echo ' + str(id) + ' > ' + myidPath)

def add():
    newPath = os.path.join(path, "conf")
    if not exists(newPath, use_sudo=False):
        print red('The path is wrong')
    else:
        print green('The path is right')
        with cd(newPath):
            if exists(os.path.join(newPath, 'zoo.cfg'), use_sudo=False):
                print green('zoo.cfg exists')
                run('cp zoo.cfg zoo.cfg_backup')

        put(confPath, newPath)
        put(myidPath, '~')

        # svstat /service/zookeeper
        # svc -t /service/zookeeper restart
        # svc -u /service/zookeeper start
        # svc -d /service/zookeeper stop
        # sudo('rm -rf /service/zookeeper/supervise')
        # sudo('cp ' + '~/myid' + " " +  os.path.join(path, 'data', 'myid'))
        run('cp ' + '~/myid' + " " +  os.path.join(path, 'data', 'myid'))
        run('svc -u ~/svc/zookeeper')
        run(os.path.join(path, 'bin', 'zkServer.sh') + ' restart')
        
def delete():
    newPath = os.path.join(path, "conf")
    if not exists(newPath, use_sudo=False):
        print red('The path is wrong')
    else:
        print green('The path is right')
        # svstat /service/zookeeper
        # svc -t /service/zookeeper restart
        # svc -u /service/zookeeper start
        # svc -d /service/zookeeper stop
        # sudo('rm -rf /service/zookeeper/supervise')
        # sudo('cp ' + '~/myid' + " " +  os.path.join(path, 'data', 'myid'))
        run('svc -d ~/svc/zookeeper')
        run(os.path.join(path, 'bin', 'zkServer.sh') + ' stop')
