from optparse import make_option
from django.core.management.base import NoArgsCommand
import sys
import os

import logging

class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
        )

    def handle_noargs(self, **options):
        from core.models import Domain
        from core.views import search
        print "running"
        from django.test import Client
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')

        f = open("/tmp/domains.txt")
        data = f.readlines()

        for x in data:
            try:
                c.post("/search", {"domain":x})
            except Exception, e :
                print "===========%s fucked up" % x


        print "done"

