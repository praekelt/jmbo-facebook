import urllib

from django import template
from django.contrib.sites.models import get_current_site
from django.conf import settings

register = template.Library()


@register.tag
def facebook_oauth_url(parser, token):
    return FacebookOauthUrlNode()


class FacebookOauthUrlNode(template.Node):

    def render(self, context):
        site = get_current_site(context['request'])
        protocol = 'http%s' % (context['request'].is_secure() and 's' or '')
        di = dict(
            redirect_uri=urllib.quote(
                '%s://%s/admin/jmbo_facebook/handler' % (protocol, site.domain)
            ),
            client_id=settings.JMBO_FACEBOOK['app_id']
        )
        url = 'https://www.facebook.com/dialog/oauth?client_id=%(client_id)s&redirect_uri=%(redirect_uri)s&scope=manage_pages' % di
        return url
