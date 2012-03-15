from django.db import models
from djangotoolbox.fields import EmbeddedModelField, ListField

class CompanyConfiguration(models.Model):
    company_id = models.TextField()
    solr_configuration = EmbeddedModelField('SolrConfiguration')

class SolrConfiguration(models.Model):
    url = models.URLField()
    parameters = ListField(EmbeddedModelField('SolrParameter'))
    default_page_size = models.IntegerField()

class SolrParameter(models.Model):
    key = models.TextField()
    value = models.TextField()