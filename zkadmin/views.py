from django.shortcuts import render_to_response
from django.conf import settings

from django.http import HttpResponse
from django import forms
from zkadmin.models import Idle
import os
from zookeeper_dashboard.zkadmin.models import ZKServer

ZOOKEEPER_SERVERS = getattr(settings,'ZOOKEEPER_SERVERS').split(',')

def index(request):
    server_data = []
    for i, server in enumerate(ZOOKEEPER_SERVERS):
        zkserver = ZKServer(server)
        zkserver.id = i
        server_data.append(zkserver)

    return render_to_response('zkadmin/index.html',
                              {'ZOOKEEPER_SERVERS':ZOOKEEPER_SERVERS,
                               'server_data':server_data})

def detail(request, server_id):
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

def idleDeploy(request):
    ip = request.GET.get('ip')
