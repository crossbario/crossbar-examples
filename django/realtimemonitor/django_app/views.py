# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django_app.models import Client
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

@csrf_exempt
def clients(request):
    """ Retrieve a client config from DB and send it back to the client """
    client, created = Client.objects.get_or_create(ip=request.POST['ip'])
    return HttpResponse(json.dumps(model_to_dict(client)), content_type='application/json')