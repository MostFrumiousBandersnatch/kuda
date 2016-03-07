# -*- coding: utf-8 -*-
"""
Parse rss feed and import its content into agenda models
"""
import sys

from django.core.management.base import BaseCommand

from agenda.utils import import_feed


class Command(BaseCommand):
    help = __doc__
    args = '<path to feed>'

    def handle(self, *args, **kwargs):
        try:
            path_to_feed = sys.argv[2]
        except ValueError:
            print self.args
            exit(1)

        try:
            with open(path_to_feed) as f:
                import_feed(f)
        except IOError:
            print 'Incorrect path_to_feed'
            exit(1)
