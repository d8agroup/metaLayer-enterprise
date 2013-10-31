TEMPLATE_STRINGS = {
    'login':{
        'header':'Upstream Analytics - Login',
        'welcome_message':'',
        'form_label_username':'Your E-mail Address',
        'form_label_password':'Your Password',
        'form_submit_button':'Login',
        'form_errors_no_username_or_password':'You must provide a username and password.',
        'form_errors_incorrect_username_or_password':'Sorry we didn\'t recognize that username and password.',
        'form_errors_user_inactive':'Sorry, your account is not currently active.',
        'form_errors_user_type_not_supported':'For some reason we can\'t create your user account. Please contact your system administrator.'
    },
    'manage_company':{
        'form_error_display_name':'You must enter the company\'s display name.',
        'form_error_display_name_used':'Sorry, there is already a company in our system with that display name, please choose a different name.',
        'form_errors_company_not_found':'Sorry, we can\'t find that company. Please contact your system administrator.',
    },
    'manage_company_api_keys':{
        'message_api_keys_saved':'The API keys were updated.'
    },
    'manage_user':{
        'h3_edit':'Edit User:',
        'h3_create':'Create New User',
        'h5_create_email_messages':'Once the user has been successfully created, they will be sent an e-mail with their password and login instructions.',
        'form_label_username':'E-mail address.',
        'form_label_password':'Password.',
        'form_label_password_edit':'Update password or leave blank.',
        'form_label_first_name':'First Name',
        'form_label_last_name':'Last Name',
        'form_action_cancel':'Cancel',
        'form_action_save':'Save',
        'message_user_created':'The user: %s was created.',
        'message_user_saved':'The user: %s was saved.',
        'form_error_email_regex':'The e-mail address you entered is not a valid e-mail.',
        'form_error_password':'The password must be letters and numbers only and at least six characters long.',
        'form_error_first_name':'First name should only contain letter.',
        'form_error_last_name':'Last name should only contain letter.',
        'form_error_user_exists':'Sorry, a user with that email address already exists.',
        'form_error_user_not_exists':'Sorry, there was an error saving that user.',
    },
    'manage_project':{
        'h3_edit':'Edit this project:',
        'form_section_basic':'Basic project details',
        'form_section_members':'Users',
        'form_section_config':'Muxboard Configuration',
        'form_section_config_help':'The settings choosen here control the various widgets available to project members.',
        'form_label_project_name':'Project Name',
        'form_label_project_description':'Project Description',
        'form_label_project_members':'Project Members',
        'form_label_project_data_points':'Data Points available to this project',
        'form_label_project_actions':'Actions available to this project',
        'form_label_project_outputs':'Outputs available to this project',
        'form_label_project_visualizations':'Visualizations available to this project',
        'form_action_cancel':'Cancel',
        'form_action_save':'Save',
        'form_action_delete':'Delete',
        'button_add_new_user':'create a new user',
        'message_project_saved':'Your changes to the project: "%s" were saved.',
        'message_project_inactive':'Project: "%s" has been deleted.',
        'form_errors_display_name':'You must enter a name for this project',
        'form_errors_description':'You must enter a description for this project',
    },
    'view_project':{
        'message_not_project_member':'Sorry, you are not a member of the project you tried to view.',
        'message_insight_deleted':'Insight successfully deleted',
        'members_header':'Project Members',
        'members_this_project_has_none':'This project has no members',
        'heading_project_activity':'Project Activity',
        'insights_header':'Project Insights',
        'insights_create_button':'Create a new insight',
        'insights_edit_button':'View in dashboard mode',
        'insights_remix_button':'Create new dashboard from this insight',
        'insights_delete_button':'Delete this insight',
   },
    'company_home':{
        'title_projects':'Your Company\'s Projects',
        'button_title_create_new_project':'Click here to create a new project for your company.',
        'title_members':'Your Company\'s Members',
        'button_title_create_new_user':'Click here to add a new member.',
        'button_title_edit_user':'Edit this user'
    },
    'change_password':{
        'h3':'Change Your Password',
        'h5':'Passwords must be at least six characters long and contain only letters, numbers and underscores',
        'label_current_password':'Your Current Password',
        'label_new_password_1':'Your New Password',
        'label_new_password_2':'Your New Password Again',
        'form_action_cancel':'Cancel',
        'form_action_save':'Save',
        'form_errors_incomplete':'All fields are required',
        'form_errors_current_password':'Your current password is incorrect',
        'form_errors_new_password_match':'The new passwords you entered do not match',
        'form_errors_new_password_strength':'Passwords must be at least six characters long and contain only letters, numbers and underscores',
        'messages_password_saved':'Your password has been updated',
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