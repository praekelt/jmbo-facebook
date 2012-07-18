from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns(
    '',

    (
        r'^admin/jmbo_facebook/handler/$',  
        'jmbo_facebook.admin_views.handler',
        {},
        'jmbo-facebook-handler',
    ),

)
