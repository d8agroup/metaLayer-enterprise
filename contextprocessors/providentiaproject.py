from companies.controllers import CompaniesController, ProjectsController

def context_providentiaproject(request):
    user = request.user
    if not user:
        return {}

    company = CompaniesController.IdentifyCompanyForUser(user)
    if not company:
        return {}

    projects = [p for p in company.projects if user.id in p.members]
    if not projects:
        return {}

    project = projects[0]
    return {
        'project':project
    }