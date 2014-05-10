from django.shortcuts import render_to_response
from django.conf import settings

from django.http import HttpResponse
from django import forms
from zkadmin.models import Idle, Server
import os
from zookeeper_dashboard.zkadmin.models import ZKServer
import logging  
import shutil 
import os
import tempfile
from subprocess import call

logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.DEBUG)  

# ZOOKEEPER_SERVERS = getattr(settings,'ZOOKEEPER_SERVERS').split(',')

def get_zookeeper_servers():
    servers = Server.objects.all()
    ZOOKEEPER_SERVERS = []
    for server in servers:
        ZOOKEEPER_SERVERS.append(server.ip.encode('ascii') + ":" + server.port.encode('ascii'))
    return ZOOKEEPER_SERVERS

def index(request):
    server_data = []
    ZOOKEEPER_SERVERS = get_zookeeper_servers()
    for i, server in enumerate(ZOOKEEPER_SERVERS):
        print i, server
        zkserver = ZKServer(server)
        zkserver.id = i
        server_data.append(zkserver)

    return render_to_response('zkadmin/index.html',
                              {'ZOOKEEPER_SERVERS':ZOOKEEPER_SERVERS,
                               'server_data':server_data})

def detail(request, server_id):
    ZOOKEEPER_SERVERS = get_zookeeper_servers()
    server_data = ZKServer(ZOOKEEPER_SERVERS[int(server_id)])
    server_data.id = server_id
    return render_to_response('zkadmin/detail.html',
                              {'server_data':server_data})

class IdleForm(forms.Form):
    ip = forms.IPAddressField()
    user = forms.CharField()
    pwd = forms.CharField(widget=forms.PasswordInput)
    path = forms.CharField()

def live(ip):
    response = os.system("ping -c 1 " + ip)
    if response == 0:
        return True
    else:
        return False

def idle(request):
    idle_data = {}
    if request.method == 'POST':
        idf = IdleForm(request.POST)
        if idf.is_valid():
            idf_data = idf.cleaned_data
            idle_m = Idle.objects.filter(ip = idf_data['ip'])  
            if not idle_m:
                idle_m = Idle(ip = idf_data['ip'], user = idf_data['user'], pwd = idf_data['pwd'], path = idf_data['path'])
                idle_m.save()

            idf = IdleForm()
            idles = Idle.objects.all()
            for i in idles:
                if live(i.ip):
                    idle_data[i.ip] = 'online'
                else:
                    idle_data[i.ip] = 'offline'
            return render_to_response('zkadmin/idle.html', {'idle_data': idle_data, 'idf': idf})
    else:
        idf = IdleForm()
    
    idles = Idle.objects.all()
    for i in idles:
        if live(i.ip):
            idle_data[i.ip] = 'online'
        else:
            idle_data[i.ip] = 'offline'
    return render_to_response('zkadmin/idle.html', {'idle_data': idle_data, 'idf': idf})

def idleDelete(request):
    t = Idle.objects.all()
    idle_m = Idle.objects.filter(ip = request.GET.get('ip'))
    if idle_m:
        idle_m.delete()

    idle_data = {}
    idles = Idle.objects.all()

    for i in idles:
        if live(i.ip):
            idle_data[i.ip] = 'online'
        else:
            idle_data[i.ip] = 'offline'

    idf = IdleForm()
    return render_to_response('zkadmin/idle.html', {'idle_data': idle_data, 'idf': idf})


# generate new config files
# TODO: port and others are changeable
def deployHelper(action, server_data=None):
    print 'deployHelper', action
    # path = '/home/kevin/Softwares/zookeeper-3.4.6/conf/'
    path = ''
    src = os.path.join(path, 'zoo.cfg')
    target = os.path.join(path, 'zoo.cfg_backup')
    tmp = tempfile.mktemp()
    shutil.copyfile(src, target)

    servers = Server.objects.all()
    count = 0
    fr = open(src, 'r')
    fw = open(tmp, 'w')
    
    for line in fr:
        if line.find('server') != -1 and count == 0:
            count += 1
            for server in servers:
                fw.write('server.' + str(count) + "=" + server.ip + ":4444:4445\n")
                count += 1
        elif line.find('server') == -1:
            fw.write(line)

    fr.close()
    fw.close()
    shutil.copyfile(tmp, src)
    
    count = 0
    for server in servers:
        count += 1
        fw = open('hostsetting.py', 'w')
        fw.write('host = "' + server.user + "@" + server.ip + '"\n')
        fw.write('password = "' + server.pwd + '"\n')
        fw.write('path = "' + server.path + '"\n')
        print 'id = ', str(count)
        fw.write('id = ' + str(count) + '\n')
        fw.close()
        call(["fab", 'add'])
    
    if action ==  'delete':
        fw = open('hostsetting.py', 'w')
        fw.write('host = "' + server_data['user'] + "@" + server_data['ip'] + '"\n')
        fw.write('password = "' + server_data['pwd'] + '"\n')
        fw.write('path = "' + server_data['path'] + '"\n')
        fw.close()
        call(['fab', 'delete'])
        

# TODO: deal with failure
# TODO: make port changeable
# TODO: security
# idleDeploy and serverDelete response should be consistent
def idleDeploy(request):
    t = Idle.objects.all()
    ip = request.GET.get('ip')
    idle_m = Idle.objects.filter(ip = ip)
    logging.debug('idleDeploy %s', idle_m[0].ip)
    
    server_m = Server.objects.filter(ip=ip)
    if server_m:
        return HttpResponse("OK")
    
    server = Server(ip=idle_m[0].ip, port="2181", user=idle_m[0].user, pwd=idle_m[0].pwd, path=idle_m[0].path)
    server.save()
    idle_m[0].delete()
    print "idleDeploy deployed"
    deployHelper('add')
    return HttpResponse("OK")

# TODO: deal with failure
def serverDelete(request):
    ip = request.GET.get('ip')
    server_m = Server.objects.filter(ip=ip)
    server = {}
    server['user'] = server_m[0].user
    server['ip'] = server_m[0].ip
    server['pwd'] = server_m[0].pwd
    server['path'] = server_m[0].path
    server_m[0].delete()

    deployHelper('delete', server)
    print 'serverDelete done'
    return HttpResponse("<script>location = location.href.substr(0, 25)</script>")

