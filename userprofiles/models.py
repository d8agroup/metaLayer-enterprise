from django.contrib.auth.models import User
from django.db import models
from djangotoolbox.fields import DictField, ListField

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    linked_accounts = DictField()
    api_keys = ListField()
    registration_code = models.TextField()
    registration_status = models.TextField()
    contact_options = DictField()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
