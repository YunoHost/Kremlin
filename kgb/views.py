# encoding: utf-8

import requests
from time import sleep
#from django.shortcuts import render
from django.http import HttpResponse
from docker import Client


def check_container_is_ready_to_be_installed(ip):
    for i in range(10):
        try:
            print "try to get the api for the %s time" % i
            installed = requests.get("https://%s/ynhapi/installed" % ip, verify=False).json()["installed"]
        except requests.ConnectionError as e:
            print "ConnectionError", e
            sleep(10)
            continue
        except ValueError as e:
            print "ValueError (probably json stuff)", e
            sleep(10)
            continue

        print "Return not installed where installed =", installed
        return not installed

    print "Fail to get api, return"
    return False


def install_docker(request, domain, password):
    print "create docker client"
    client = Client(base_url='unix://var/run/docker.sock', version='1.6', timeout=10)
    print "create container"
    container = client.create_container("yunohost", tty=True, detach=True, command="/sbin/init")
    print "start container"
    client.start(container["Id"])
    print "get ip"
    ip = client.inspect_container(container["Id"])["NetworkSettings"]["IPAddress"]
    print "the ip", ip

    #from ipdb import set_trace; set_trace()
    if not check_container_is_ready_to_be_installed(ip):
        return HttpResponse("ça a merdé caca prout")

    print "Post on the api"
    requests.post("https://%s/ynhapi/postinstall" % ip, data={"domain": domain, "password": password}, verify=False)

    return HttpResponse(u"Youpi, ça a marché ! %s" % ip)
