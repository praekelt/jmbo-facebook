import urllib2

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib import messages
from django.conf import settings

from jmbo_facebook.models import Page


@staff_member_required
def handler(request):
    path_info = context['request'].META['PATH_INFO']
    redirect = HttpResponseRedirect(path_info)

    code = request.REQUEST.get('code')
    if not code:
        # Nothing to do
        return redirect

    # Exchange code for an access token
    site = get_current_site(request)
    protocol = 'http%s' % (request.is_secure() and 's' or '')
    di = dict(
        redirect_uri=urllib.quote(
            '%s://%s%shandler' % (protocol, site.domain, path_info)
        ),
        client_id=settings.JMBO_FACEBOOK['app_id'],
        client_secret=settings.JMBO_FACEBOOK['app_secret'],
        code=code
    )

    url = 'https://graph.facebook.com/oauth/access_token?client_id=%(client_id)s&redirect_uri=%(redirect_uri)s&client_secret=%(client_secret)s&code=%(code)s' \
        % di
    try:
        response = urllib2.urlopen(url)
    except Exception, e:
        # Blindly catch exceptions
        msg = "Something went wrong. Headers: %s" % str(e.headers.items())
        messages.error(request, msg, fail_silently=True)
        return redirect

    # Read json from response
    json = simplejson.loads(response.read())

    # Create / update pages
    for di in json['data']:
        facebook_id = di['id']
        page, dc = Page.objects.get_or_create(facebook_id=facebook_id).exists()
        page.title = di['name']
        page.access_token = di['access_token']
        page.save()

    msg = "Created / updated pages. You must publish the relevant pages."
    messages.success(request, msg, fail_silently=True)
    return redirect
