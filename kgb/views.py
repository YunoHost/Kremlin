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
            response = requests.get("https://%s/ynhapi/installed" % ip, verify=False)
            installed = response.json()["installed"]
        except requests.ConnectionError as e:
            print "ConnectionError", e
            sleep(10)
            continue
        except ValueError as e:
            print "ValueError (probably json stuff)", e, [response.content]
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
    try:
        response = requests.post("https://%s/ynhapi/postinstall" % ip, data={"domain": domain, "password": password}, verify=False)
    except requests.ConnectionError as e:
        # check that the response is empty because in YUNOHOST world, a success
        # is indicated by an empty response that doesn't even respect HTTP
        # standard because YOLO SWAG
        if e.args[0].reason.line != "":
            raise e
    else:
        if response.status_code != 200:
            print response.content
            print response.json()
            return HttpResponse(u"Sa mère ça a merdé")

    return HttpResponse(u"Youpi, ça a marché ! %s" % ip)
