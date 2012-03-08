import random
import string
from companies.forms import validate_company
from companies.models import Company, Project
from companies.utils import user_is_company_admin
import constants
from themanager.forms import clean_and_validate_project_form

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

    @classmethod
    def AddUserToCompany(cls, company, user):
        company = cls.GetCompanyById(company.id)
        if user.id not in company.members:
            company.members.append(user.id)
            company.save()

    @classmethod
    def IdentifyCompanyForUser(cls, user):
        candidate_companies = [c for c in Company.objects.all() if user.id in c.members]
        if candidate_companies:
            return candidate_companies[0]
        return None


class ProjectsController(object):
    @classmethod
    def GetCompanyProjectsForUser(cls, company, user, only_active=True):
        projects = company.projects
        if only_active:
            projects = [p for p in projects if p.active == True]
        if not user_is_company_admin(user, company):
            projects = [p for p in projects if user.id in p.members]
        return projects

    @classmethod
    def CreateNewProjectInCompany(cls, company):
        company = CompaniesController.GetCompanyById(company.id)
        project = Project(
            display_name='Project %i' % (len(company.projects) + 1),
            project_id="".join([random.choice(string.letters) for i in xrange(15)])
        )
        company.projects.append(project)
        company.save()
        return project

    @classmethod
    def GetProjectById(cls, company, user, id):
        company = CompaniesController.GetCompanyById(company.id)
        for project in company.projects:
            if project.project_id == id:
                if user_is_company_admin(user, company) or user.id in project.members:
                    return project
        return None

    @classmethod
    def UpdateProjectFromFormValues(cls, project_id, company, values):
        passed, errors, clean_values = clean_and_validate_project_form(values)
        if not passed:
            return False, errors

        company = CompaniesController.GetCompanyById(company.id)
        project = [p for p in company.projects if p.project_id == project_id][0]
        for key, value in clean_values.items():
            try:
                setattr(project, key, value)
            except AttributeError:
                continue

        company.save()
        return True, []

