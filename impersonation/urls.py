from django.conf.urls import patterns, url

from impersonation.views import ImpersonateView

urlpatterns = patterns('',
                       url(r"^login/(?P<user_model>[\w\.]+)/(?P<pk>\d+)$",
                           ImpersonateView.as_view(),
                           name="impersonate_user"),
                       )
