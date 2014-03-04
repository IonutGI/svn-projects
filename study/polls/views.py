# Create your views here.

from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import BaseCreateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from polls.models import Poll, Choice

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


def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render_to_response("polls/polls_results.html", {"poll": poll})
#===============================================================================
#                                CBV
#===============================================================================


class PollList(ListView):
    model  = Poll
    template_name = "polls_list.html"

    def get_context_data(self, **kwargs):
        context = super(PollList, self).get_context_data(**kwargs)
        context["polls_list"] = Poll.objects.all()
        return context


class PollIndex(TemplateView):
    
    model = Poll
    template_name = "polls_index.html"

    @staticmethod
    def latest5(self):
        return Poll.objects.order_by("-pub_date")[:5]

    def get_context_data(self, **kwargs):
        context = super(PollIndex, self).get_context_data(**kwargs)
        context["latest_poll_list"] =PollIndex.latest5()
        return context


class PollVote(BaseCreateView):
    """
        Vote choice for selected Poll.

        Retrieve selected Poll.
        Retrieve Choice set for Selected Poll.
        Return error message if error.
        Update votes for current choice.
    """
    model = Poll
    template_name = None

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(PollVote, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=kwargs["poll_id"])
        try:
            selected_choice = poll.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            context = {
                "poll": poll,
                "error_message": "You didn't select a choice."
            }
            return render_to_response("polls/polls_detail.html", context)
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse("polls:poll-results", args=(poll.id,)))


class PollDetail(DetailView):
    model = Poll
    template_name = "polls_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PollDetail, self).get_context_data(**kwargs)
        try:
            # context["poll"] = Poll.objects.get(pk=kwargs["object"].id)
            context["poll"] = get_object_or_404(Poll, pk=kwargs["object"].id)
        except Poll.DoesNotExist as error:
            logger.error("Query Error. %(error)s" % {"error": error})
            raise Http404
        return context