from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class EmailController(object):
    def __init__(self, company=None):
        self.company = company

    def send_new_user_created_email(self, user, password):
        template_data = {
            'user':user,
            'user_password':password,
            'company':self.company or self._base_company_data(),
            'site_host':settings.SITE_HOST
        }
        subject = 'You have been invited to join metaLayer'
        from_email = 'Team Metalayer <no-reply@metalayer.com>'
        html = render_to_string(
            'emails/new_user_created.html',
            template_data
        )
        text = strip_tags(html)
        msg = EmailMultiAlternatives(subject, text, from_email, [user.email])
        msg.attach_alternative(html, "text/html")
        msg.send()

    def _base_company_data(self):
        return {
            'display_name':'metaLayer'
        }




