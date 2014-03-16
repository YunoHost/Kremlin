# encoding: utf-8

#from django.shortcuts import render
from django.http import HttpResponse
from models import Container


def install_docker(request, domain, password):
    container = Container.create_new_container(domain, password)
    return HttpResponse(u"Youpi, ça a marché ! %s" % container.ip)
