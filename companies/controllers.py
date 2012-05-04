import random
import string
from companies.forms import validate_company, clean_and_validate_project_form, clean_and_validate_company_api_keys_form
from companies.models import Company, Project, ActivityRecord, ActivityDetails
from companies.utils import user_is_company_admin
import constants
from metalayercore.actions.controllers import ActionController
from metalayercore.datapoints.controllers import DataPointController

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
        except Company.DoesNotExist:
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
    def GetAllCompanies(cls, include_deleted=False):
        if include_deleted:
            return Company.objects.all()
        return Company.objects.filter(deleted=False)

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
        candidate_companies = [c for c in Company.objects.all() if user.id in c.members or user.id in c.administrators]
        if candidate_companies:
            return candidate_companies[0]
        return None

    @classmethod
    def DeleteCompanyById(cls, id):
        company = cls.GetCompanyById(id)
        if company:
            company.deleted = True
            company.save()

    @classmethod
    def GetCompanyAPIKeys(cls, id):
        company = cls.GetCompanyById(id)
        api_keys = []
        if company:
            for data_point_type in company.data_points_available:
                data_point = DataPointController.LoadDataPoint(data_point_type)
                if len([e for e in data_point.get_unconfigured_config()['elements'] if e['type'] == 'api_key']):
                    api_key = {
                        'type':data_point_type,
                        'display_name':DataPointController.LoadDataPoint(data_point_type).get_unconfigured_config()['full_display_name'],
                        'help':DataPointController.ExtractAPIKeyHelp(data_point_type)
                    }
                    if data_point_type in company.api_keys:
                        api_key['api_key'] = company.api_keys[data_point_type]
                    api_keys.append(api_key)
            for action_name in company.actions_available:
                action = ActionController.LoadAction(action_name)
                if len([e for e in action.get_unconfigured_config()['elements'] if e['type'] == 'api_key']):
                    api_key = {
                        'type':action_name,
                        'display_name':ActionController.LoadAction(action_name).get_unconfigured_config()['display_name_long'],
                        'help':ActionController.ExtractAPIKeyHelp(action_name)
                    }
                    if action_name in company.api_keys:
                        api_key['api_key'] = company.api_keys[action_name]
                    api_keys.append(api_key)
        return api_keys

    @classmethod
    def UpdateCompanyAPIKeysFromFormValues(cls, id, values):
        company = cls.GetCompanyById(id)
        if not company:
            return False, [constants.TEMPLATE_STRINGS['manage_company']['form_errors_company_not_found']]

        passed, errors, clean_values = clean_and_validate_company_api_keys_form(cls.GetCompanyAPIKeys(id), values)
        company.api_keys = clean_values
        company.save()



class ProjectsController(object):
    @classmethod
    def GetCompanyProjectsForUser(cls, company, user, only_active=True):
        projects = company.projects
        if only_active:
            projects = [p for p in projects if p.active == True]
        if not user_is_company_admin(user, company):
            projects = [p for p in projects if user.id in p.members]
        projects = sorted(projects, key=lambda p: p.created, reverse=True)
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

    @classmethod
    def AddInsightToProject(cls, company, project_id, insight_id):
        company = CompaniesController.GetCompanyById(company.id)
        project = [p for p in company.projects if p.project_id == project_id][0]
        if insight_id not in project.insights:
            project.insights.append(insight_id)
        company.save()

    @classmethod
    def MarkProjectAsInactive(cls, company, project_id):
        company = CompaniesController.GetCompanyById(company.id)
        project = [p for p in company.projects if p.project_id == project_id][0]
        project.active = False
        company.save()

class ActivityRecordsController(object):
    @classmethod
    def _Record_Activity(cls, activity_message_key, activity_type, company, project, user, insight=None, secondary_user=None):
        record = ActivityRecord(user_id=user.id)
        if company and project:
            record.company_id = company.id
            record.project_id = project.project_id
            record.activity_level = 1 if user.id in company.administrators else 2
            record.activity_details = ActivityDetails(
                username=user.username,
                company_display_name=company.display_name,
                project_display_name=project.display_name,
                activity_type=activity_type,
                activity_message_key=activity_message_key,
            )
        elif company:
            record.company_id = company.id
            record.activity_level = 1 if user.id in company.administrators else 2
            record.activity_details = ActivityDetails(
                username=user.username,
                company_display_name=company.display_name,
                activity_type=activity_type,
                activity_message_key=activity_message_key,
            )
        else:
            record.activity_level = 0
            record.activity_details = ActivityDetails(
                username=user.username,
                activity_type=activity_type,
                activity_message_key=activity_message_key,
            )
        if insight:
            record.insight_id = insight.id
            record.activity_details.insight_name = insight.name
        if secondary_user:
            record.activity_details.secondary_username = secondary_user.username
        record.save()

    @classmethod
    def _FormatActivityRecord(cls, activity_record):
        message = constants.ACTIVITY_TEXT[activity_record.activity_details.activity_message_key]
        replacement_pairs = (
            ('{USERNAME}', 'username'),
            ('{PROJECT_DISPLAY_NAME}', 'project_display_name'),
            ('{INSIGHT_NAME}', 'insight_name'),
            ('{SECONDARY_USERNAME}', 'secondary_username')
        )
        for pair in replacement_pairs:
            try:
                message = message.replace(pair[0], getattr(activity_record.activity_details, pair[1]))
            except TypeError:
                pass
        return {
            'css_class':activity_record.activity_details.activity_type,
            'date':activity_record.date,
            'message':message,
        }

    @classmethod
    def RecordLogin(cls, user, company=None, project=None):
        activity_type = 'user'
        activity_message_key = 'user_login'
        cls._Record_Activity(activity_message_key, activity_type, company, project, user)

    @classmethod
    def RecordUserSaved(cls, user, company=None, project=None, secondary_user=None):
        activity_type = 'user'
        activity_message_key = 'user_saved'
        cls._Record_Activity(activity_message_key, activity_type, company, project, user, secondary_user=secondary_user)

    @classmethod
    def RecordUserCreated(cls, user, company=None, project=None, secondary_user=None):
        activity_type = 'user'
        activity_message_key = 'user_created'
        cls._Record_Activity(activity_message_key, activity_type, company, project, user, secondary_user=secondary_user)

    @classmethod
    def RecordProjectCreated(cls, user, company=None, project=None):
        activity_type = 'project'
        activity_message_key = 'project_new'
        cls._Record_Activity(activity_message_key, activity_type, company, project, user)

    @classmethod
    def RecordProjectSaved(cls, user, company=None, project=None):
        activity_type = 'project'
        activity_message_key = 'project_save'
        cls._Record_Activity(activity_message_key, activity_type, company, project, user)

    @classmethod
    def RecordInsightCreated(cls, user, company=None, project=None):
        activity_type = 'insight'
        activity_message_key = 'insight_created'
        cls._Record_Activity(activity_message_key, activity_type, company, project, user)

    @classmethod
    def RecordInsightEdited(cls, user, company=None, project=None, insight=None):
        activity_type = 'insight'
        activity_message_key = 'insight_edited'
        cls._Record_Activity(activity_message_key, activity_type, company, project, user, insight)

    @classmethod
    def RecordInsightRemixed(cls, user, company=None, project=None, insight=None, secondary_user=None):
        activity_type = 'insight'
        activity_message_key = 'insight_remixed'
        cls._Record_Activity(activity_message_key, activity_type, company, project, user, insight, secondary_user)

    @classmethod
    def GetAndFormatCompanyWideActivity(cls, user, company, count=10):
        activity_level = 0 if user_is_company_admin(user, company) else 1
        activity_records = ActivityRecord.objects.filter(company_id=company.id)
        activity_records = [a for a in activity_records if a.activity_level > activity_level]
        activity_records = sorted(activity_records, key=lambda a: a.date, reverse=True)
        formatted_activity_records = [cls._FormatActivityRecord(a) for a in activity_records]
        return formatted_activity_records

    @classmethod
    def GetAndFormatProjectWideActivity(cls, user, company, project_id, count=10):
        activity_level = 0 if user_is_company_admin(user, company) else 1
        activity_records = ActivityRecord.objects.filter(project_id=project_id).filter(activity_level__gte=activity_level)
        activity_records = sorted(activity_records, key=lambda a: a.date, reverse=True)
        formatted_activity_records = [cls._FormatActivityRecord(a) for a in activity_records[:count]]
        return formatted_activity_records





