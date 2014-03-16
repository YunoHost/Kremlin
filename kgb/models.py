# encoding: utf-8

import os
import requests
from docker import Client
from django.db import models
from django.conf import settings
from .utils import check_container_is_ready_to_be_installed


class Container(models.Model):
    ip = models.GenericIPAddressField(protocol="IPv4", unique=True, null=True)
    ip6 = models.GenericIPAddressField(protocol="IPv6", unique=True, null=True)
    docker_id = models.CharField(max_length=255, unique=True, null=True)
    domain = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_available_ips(klass):
        used_ips = set([x.ip for x in klass.objects.all()])
        available_public_ips = set(settings.AVAILABLE_PUBLIC_IPS)
        return sorted(list(available_public_ips - used_ips))

    @classmethod
    def create_new_container(klass, domain, password):
        # XXX here, possible race condition where 2 thread get the same ip then
        # try to save in db, the db will raise an integrity error on the
        # slowest thread because the ip column is unique
        # FIXME use something like "with thread.lock: ..."
        ip = klass.get_available_ips()[0]
        print "Use the ip:", ip
        container = klass.objects.create(ip=ip, domain=domain, docker_id=None)
        docker_id = container.create_docker(domain=domain, password=password, public_ip=ip)
        container.docker_ip = docker_id
        container.save()
        return container

    def create_docker(self, domain, password, public_ip):
        print "create docker client"
        client = Client(base_url='unix://var/run/docker.sock', version='1.6', timeout=10)
        print "create container"
        container = client.create_container("yunohost", tty=True, detach=True, command="/sbin/init")
        print "start container"
        client.start(container["Id"])
        print "get ip"
        ip = client.inspect_container(container["Id"])["NetworkSettings"]["IPAddress"]
        print "the ip", ip

        check_container_is_ready_to_be_installed(ip)

        print "Post on the api"
        try:
            response = requests.post("https://%s/ynhapi/postinstall" % ip, data={"domain": domain, "password": password}, verify=False)
        except requests.ConnectionError as e:
            # check that the response is empty because in YUNOHOST world, a success
            # is indicated by an empty response that doesn't even respect HTTP
            # standard because YOLO SWAG
            if e.args[0].reason.line != "''":
                raise e
        else:
            if response.status_code != 200:
                print response.content
                print response.json()
                # TODO raise
                #return HttpResponse(u"Sa mère ça a merdé")

        os.system("iptables -t nat -A PREROUTING -d 192.168.2.11 -j DNAT --to-destination %s" % ip)
        os.system("iptables -t nat -A POSTROUTING -s '%s/32' -o eth0 -j SNAT --to-source 192.168.2.11" % ip)

        return container["Id"]
