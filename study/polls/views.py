# Create your views here.

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView

from polls.models import Poll

import logging

logger = logging.getLogger(__name__)
#===============================================================================
#                                FBV
#===============================================================================
def index(request):
    latest_poll_list = Poll.objects.order_by("-pub_date")[:5]
    template_name = "polls/polls_index.html"
    context = {"latest_poll_list": latest_poll_list}
    return render(request, template_name, context)

def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    template_name = "polls/polls_detail.html"
    return render(request, template_name, {"poll": poll})
def results(request, poll_id):
    return HttpResponse("You're looking at the results for poll %(id)s." % {"id": poll_id})

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %(id)s." % {"id": poll_id})

#===============================================================================
#                                CBV
#===============================================================================

class PollIndex(TemplateView):
    
    model = Poll
    template_name = "polls_index.html"
    
    def latest5(self):
        return Poll.objects.order_by("-pub_date")[:5]

    def get_context_data(self, **kwargs):
        context = super(PollIndex, self).get_context_data(**kwargs)
        context["latest_poll_list"] = self.latest5()
        return context

class PollDetail(DetailView):
    model = Poll
    template_name = "polls_detail.html"

    def get_context_data(self, **kwargs):
        print kwargs
        context = super(PollDetail, self).get_context_data(**kwargs)
        try:
            context["poll"] = Poll.objects.get(pk=kwargs["object"].id)
        except Poll.DoesNotExist as error:
#             logger.error("Query Error. %(error)s" % {"error": error})
            raise Http404
        return context