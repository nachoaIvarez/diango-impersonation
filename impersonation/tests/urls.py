from django.conf.urls import patterns, url, include

urlpatterns = patterns('impersonation.tests.views',
                       url(r"^current_user/$",
                           "current_user",
                           name="current_user"),
                       url(r"^", include('impersonation.urls')),
                       )
