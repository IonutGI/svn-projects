'''
Created on Feb 16, 2014

@author: Ganea Ionut Iulian
'''

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns("",
    url(r'^$', views.index, name="index")
)
