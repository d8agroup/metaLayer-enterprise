TEMPLATE_STRINGS = {
    'login':{
        'header':'Login',
        'welcome_message':'Welcome to MetaLayer, please log in with your email address and password',
        'form_label_username':'Your email address',
        'form_label_password':'Your password',
        'form_submit_button':'login',
        'form_errors_no_username_or_password':'You must provide a username and password.',
        'form_errors_incorrect_username_or_password':'Sorry we didn\'t recognize that username and password combo.',
        'form_errors_user_inactive':'Sorry, your account is not currently active.',
        'form_errors_user_type_not_supported':'Sorry, we cant find a home for your user account, please contact your systems administrator.'
    },
    'manage_company':{
        'form_error_display_name':'You must enter the companies display name',
        'form_error_display_name_used':'Sorry, there is already a company in our system with that display name, please choose another',
        'form_errors_company_not_found':'Sorry we cant find that company, please contact your systems administrator.',
    },
    'manage_user':{
        'form_error_email_regex':'The email address you entered is not a valid email',
        'form_error_first_name':'First name should only contain letter',
        'form_error_last_name':'Last name should only contain letter',
        'form_error_user_exists':'Sorry, a user with that emails address already exists',
    }

}

MODEL_DEFAULTS = {
    'companies':{
        'default_display_name':'Please enter your company name'
    }
}