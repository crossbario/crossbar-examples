# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django_app.models import Client
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

@csrf_exempt
def clients(request):
    """ Retrieve a client config from DB and send it back to the client """
    ip = request.POST.get('ip', None)
    try:
    	client, created = Client.objects.get_or_create(ip=ip)
        data = model_to_dict(client)
    except Exception as e:
    	print("Could not retrieve client config for IP '{}': {}".format(ip, e))
    else:
        print("Client config for retrieved for IP '{}'".format(ip, data))
        return HttpResponse(json.dumps(data), content_type='application/json')