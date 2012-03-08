import datetime
from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField
import constants

class Company(models.Model):
    display_name = models.TextField(default=constants.MODEL_DEFAULTS['companies']['default_display_name'])
    administrators = ListField()
    members = ListField()
    projects = ListField(EmbeddedModelField('Project'))
    data_points_available = ListField()
    actions_available = ListField()
    outputs_available = ListField()
    visualizations_available = ListField()

class Project(models.Model):
    project_id = models.TextField()
    created = models.DateField(default=datetime.datetime.now())
    display_name = models.TextField()
    description = models.TextField()
    active = models.BooleanField(default=True)
    members = ListField()
    data_points_available = ListField()
    actions_available = ListField()
    outputs_available = ListField()
    visualizations_available = ListField()
    insights = ListField()