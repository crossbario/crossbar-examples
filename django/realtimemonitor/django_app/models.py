# -*- coding: utf-8 -*-

import requests

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict


class Client(models.Model):
    """ Our client configuration """

    # Client unique identifier
    ip = models.GenericIPAddressField()

    # What data to send to the dashboard
    show_cpus = models.BooleanField(default=True)
    show_memory = models.BooleanField(default=True)
    show_disk = models.BooleanField(default=True)

    # Stop sending data
    disabled = models.BooleanField(default=False)

    # Data refresh frequency
    frequency = models.IntegerField(default=1)

    def __unicode__(self):
        return self.ip


@receiver(post_save, sender=Client, dispatch_uid="server_post_save")
def notify_server_config_changed(sender, instance, **kwargs):
    """ Notifies a client that its config has changed.

        This function is executed when we save a Client model, and it
        makes a POST request on the WAMP-HTTP bridge, allowing us to
        make a WAMP publication from Django.
    """
    requests.post("http://127.0.0.1:8080/notify",
                  json={
                      'topic': 'clientconfig.' + instance.ip,
                      'args': [model_to_dict(instance)]
                  })