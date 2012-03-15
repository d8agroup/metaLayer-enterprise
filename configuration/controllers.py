from configuration.models import CompanyConfiguration

class CompanyConfigurationController(object):
    @classmethod
    def _CreateCompanyConfiguration(cls, company):
        config = CompanyConfiguration(
            company_id=company.id
        )
        config.save()
        return config

    @classmethod
    def GetSolrConfigurationForCompany(cls, company):
        try:
            config = CompanyConfiguration.objects.get(company_id=company.id)
        except CompanyConfiguration.DoesNotExist:
            config = cls._CreateCompanyConfiguration(company)
        return config.solr_configuration

    @classmethod
    def UpdateSolrConfigurationFromValues(cls, values):
        raise NotImplementedError

