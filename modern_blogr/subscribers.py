from itertools import groupby
from calendar import month_name

from pyramid.events import subscriber
from pyramid.events import BeforeRender

from .models import Entry


def _make_archives(entries):
    def grouper(entry): 
        return entry.created.year, entry.created.month

    archives = []
    for ((year, month), items) in groupby(entries, key=grouper):
        fullname = "%s %s" % (month_name[month], year)
        archives.append({'year': "%d" % year,
                         'month': "%02d" % month,
                         'fullname': fullname})
    return archives


@subscriber(BeforeRender)
def add_archives(event):
    archives = _make_archives(Entry.all())
    event.update({'archives': archives})
