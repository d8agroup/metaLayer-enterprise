def user_is_company_admin(user, company):
    if user.is_staff:
        return True
    return user.id in company.administrators