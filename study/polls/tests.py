"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.utils import timezone

from polls.models import Poll

import datetime


class PollMethodTest(TestCase):

    def test_was_published_recently_with_future_poll(self):
        # should return false for polls whose pub_date is in the future
        future_poll = Poll(pub_date=timezone.now()+datetime.timedelta(days=30))
        self.assertEqual(future_poll.published_recently(), False)

    def test_old_poll(self):
        old_poll = Poll(pub_date=timezone.now()-datetime.timedelta(days=30))
        self.assertEqual(old_poll.published_recently(), False)

    def test_recent_poll(self):
        recent_poll = Poll(pub_date=timezone.now()-datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.published_recently(), True)