TEMPLATE_STRINGS = {
    'login':{
        'header':'Login',
        'welcome_message':'',
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
        'h3_edit':'Edit User:',
        'h3_create':'Create a new User',
        'h5_create_email_messages':'Once the user has been successfully created, they will be sent an email with their password and login instructions',
        'form_label_username':'Users Email Address',
        'form_label_username':'Users Password',
        'form_label_first_name':'First Name',
        'form_label_last_name':'Last Name',
        'form_action_cancel':'Cancel',
        'form_action_save':'Save',
        'message_user_created':'The user: %s was created',
        'message_user_saved':'The user: %s was saved',
        'form_error_email_regex':'The email address you entered is not a valid email',
        'form_error_password':'The users password must be letter and numbers only at at least six characters long',
        'form_error_first_name':'First name should only contain letter',
        'form_error_last_name':'Last name should only contain letter',
        'form_error_user_exists':'Sorry, a user with that emails address already exists',
    },
    'manage_project':{
        'h3_edit':'Edit this project:',
        'form_section_basic':'Basic Project Details',
        'form_section_members':'Users',
        'form_section_config':'Insight Configuration',
        'form_section_config_help':'The settings you choose here control the widgets that are available to project members when they start to create insights.',
        'form_label_project_name':'Project Name',
        'form_label_project_description':'Project Description',
        'form_label_project_members':'Project Members',
        'form_label_project_data_points':'Data Points available to this project',
        'form_label_project_actions':'Actions available to this project',
        'form_label_project_outputs':'Outputs available to this project',
        'form_label_project_visualizations':'Visualizations available to this project',
        'form_action_cancel':'Cancel',
        'form_action_save':'Save',
        'button_add_new_user':'create a new user',
        'message_project_saved':'Your changes to the project: "%s" were saved.',
        'form_errors_display_name':'You must enter a name for this project',
        'form_errors_description':'You must enter a description for this project',
    },
    'view_project':{
        'message_not_project_member':'Sorry, you are not a member of the project you tried to view.',
        'members_header':'Project Members',
        'members_this_project_has_none':'This project has no members',
        'heading_project_activity':'Project Activity',
        'insights_header':'Project Insights',
        'insights_create_button':'Create a new insight',
        'insights_edit_button':'View in dashboard mode',
        'insights_remix_button':'Create new dashboard from this insight',
   },
    'company_home':{
        'title_projects':'Your Companies Projects',
        'button_title_create_new_project':'Click here to create a new project for your company.',
    }

}

MODEL_DEFAULTS = {
    'companies':{
        'default_display_name':'Please enter your company name'
    }
}

ACTIVITY_TEXT = {
    'user_login':'{USERNAME} logged in',
    'user_saved':'{USERNAME} updated the user {SECONDARY_USERNAME}',
    'user_created':'{USERNAME} created the user {SECONDARY_USERNAME}',
    'project_new':'{USERNAME} started creating a new project',
    'project_save':'{USERNAME} updated the project {PROJECT_DISPLAY_NAME}',
    'insight_created':'{USERNAME} created a new insight in project {PROJECT_DISPLAY_NAME}',
    'insight_edited':'{USERNAME} started editing the insight {INSIGHT_NAME} in project {PROJECT_DISPLAY_NAME}',
    'insight_remixed':'{USERNAME} remixed the insight {INSIGHT_NAME} by {SECONDARY_USERNAME} in project {PROJECT_DISPLAY_NAME}',
}