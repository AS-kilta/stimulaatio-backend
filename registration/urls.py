from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from registration import views

urlpatterns = [
    url(r'^registration/$', views.RegistrationList.as_view()),
    url(r'^registration/all$', views.RegistrationListAll.as_view()),
    url(r'^registration/(?P<pk>[0-9]+)/$', views.RegistrationDetail.as_view()),
    url(r'^registration/count', views.RegistrationCount.as_view()),
]
