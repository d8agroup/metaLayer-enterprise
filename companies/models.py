from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField
import constants

class Company(models.Model):
    display_name = models.TextField(default=constants.MODEL_DEFAULTS['companies']['default_display_name'])
    administrators = ListField()
    members = ListField()
    projects = ListField(EmbeddedModelField('Project'))

class Project(models.Model):
    display_name = models.TextField()
    description = models.TextField()
    active = models.BooleanField(default=True)
    members = ListField()