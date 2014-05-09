import shutil 
import os
import tempfile

# after save the new server
# parater new server ip
# TODO: port and others are changeable
def testAdd(ip):
    path = '/home/kevin/Softwares/zookeeper-3.4.6/conf/'
    src = os.path.join(path, 'zoo.cfg')
    target = os.path.join(path, 'zoo.cfg_backup')
    tmp = tempfile.mktemp()
    shutil.copyfile(src, target)

    # servers = Server.objects.all()
    servers = [1,2,3,4]
    count = 0
    fr = open(src, 'r')
    fw = open(tmp, 'w')
    
    for line in fr:
        fw.write(line)
        if line.find('server') != -1:
            count += 1

        if count == len(servers) - 1:
            fw.write('server.' + str(count + 1) + "=" + ip + ":4444:4445\n")
            count += 1


    fr.close()
    fw.close()
    shutil.copyfile(tmp, src)

def testDel(ip):
    path = '/home/kevin/Softwares/zookeeper-3.4.6/conf/'
    src = os.path.join(path, 'zoo.cfg')
    target = os.path.join(path, 'zoo.cfg_backup')
    tmp = tempfile.mktemp()
    shutil.copyfile(src, target)

    # servers = Server.objects.all()
    servers = [1,2,3,4]
    count = 0
    fr = open(src, 'r')
    fw = open(tmp, 'w')
    
    for line in fr:
        fw.write(line)
        if line.find('server') != -1:
            count += 1

        if count == len(servers) - 1:
            fw.write('server.' + str(count + 1) + "=" + ip + ":4444:4445\n")
            count += 1


    fr.close()
    fw.close()
    shutil.copyfile(tmp, src)

