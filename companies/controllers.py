from companies.forms import validate_company
from companies.models import Company
from companies.utils import user_is_company_admin
import constants

class CompaniesController(object):
    @classmethod
    def CreateNewEmptyCompany(cls, administrator=None):
        company = Company()
        if administrator:
            company.administrators.append(administrator.id)
        company.save()
        return company

    @classmethod
    def GetCompanyById(cls, id):
        try:
            company = Company.objects.get(id=id)
        except:
            return None
        return company

    @classmethod
    def GetCompanyByDisplayName(cls, display_name):
        try:
            company = Company.objects.get(display_name=display_name)
        except Company.DoesNotExist:
            return None
        return company

    @classmethod
    def GetAllCompanies(cls):
        return Company.objects.all()

    @classmethod
    def UpdateCompanyFromFormValues(cls, id, values):
        company = cls.GetCompanyById(id)
        if not company:
            return False, [constants.TEMPLATE_STRINGS['manage_company']['form_errors_company_not_found']]

        passed, errors, clean_values = validate_company(id, values)
        if not passed:
            return False, errors

        for key, value in clean_values.items():
            try:
                setattr(company, key, value)
            except AttributeError:
                continue

        company.save()
        return True, []

class ProjectsController(object):
    @classmethod
    def GetCompanyProjectsForUser(cls, company, user, only_active=True):
        projects = company.projects
        if only_active:
            projects = [p for p in projects if p.active == True]
        if not user_is_company_admin(user, company):
            projects = [p for p in projects if user.id in p.members]
        return projects

