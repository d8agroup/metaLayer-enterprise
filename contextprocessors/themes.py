def context_themes(request):
    #TODO this will need to get the theme from the user.company
    company = request.company
    if company and company.theme:
        theme = company.theme
    else:
        theme = 'basic'
    return {
        'theme': theme
    }