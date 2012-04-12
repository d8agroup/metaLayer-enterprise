import datetime
from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField, DictField
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
    api_keys = DictField()
    deleted = models.BooleanField(default=False)
    theme = models.TextField()

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

class ActivityDetails(models.Model):
    username = models.TextField(null=True)
    company_display_name = models.TextField(null=True)
    project_display_name = models.TextField(null=True)
    insight_name = models.TextField(null=True)
    secondary_username = models.TextField(null=True)
    activity_type = models.TextField() #user|project|insight
    activity_message_key = models.TextField() #key for constants.ACTIVITY_TEXT

class ActivityRecord(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now())
    user_id = models.TextField(null=True)
    company_id = models.TextField(null=True)
    project_id = models.TextField(null=True)
    insight_id = models.TextField(null=True)
    activity_level = models.IntegerField(default=0) #0=SuperAdmin 1=CompanyAdmin 2=User
    activity_details = EmbeddedModelField('ActivityDetails')