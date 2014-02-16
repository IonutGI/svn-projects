'''
Created on Feb 10, 2014

@author: Ganea Ionut Iulian
'''
from django.contrib import admin
from polls.models import Choice, Poll
from django.contrib.admin.templatetags.admin_list import date_hierarchy

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):

    list_display = ('question', 'pub_date', 'published_recently')
    list_filter = ["pub_date"]
    search_fields = ["question"]
    date_hierarchy = "pub_date"

    fieldsets = [
        (None, {
                    'fields': ['question'],
                 }),
         ('Date Information', {
                     'fields': ['pub_date'],
                 }),
    ]

    inlines = [ChoiceInLine]

admin.site.register(Poll, PollAdmin)