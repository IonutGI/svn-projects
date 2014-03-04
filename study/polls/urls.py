'''
Created on Feb 16, 2014

@author: Ganea Ionut Iulian
'''

from django.conf.urls import patterns, url

from polls.views import PollDetail, PollIndex, PollList, PollVote

from . import views


urlpatterns = patterns("",
    #===========================================================================
    # #FBV
    #===========================================================================
    url(r'^$', views.index, name="poll-index"),
    url(r'(?P<poll_id>\d+)/$', views.detail, name="poll-detail"),
    url(r'(?P<poll_id>\d+)/results/$', views.results, name="poll-results"),
    url(r'(?P<poll_id>\d+)/vote/$', views.vote, name="poll-vote"),

    #===========================================================================
    # #CBS
    #===========================================================================
    url(r'index/$', PollIndex.as_view(), name="cbv-poll-index"),
    url(r'(?P<pk>\d+)/detail/$', PollDetail.as_view(), name="cbv-poll-detail"),
    url(r'list/$', PollList.as_view(), name="cbv-poll-list"),
    url(r'(?P<poll_id>\d+)/cbv_vote/$', PollVote.as_view(), name="cbv-poll-vote")
)
