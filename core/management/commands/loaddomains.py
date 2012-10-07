from optparse import make_option
from django.core.management.base import NoArgsCommand
import sys
import os

import logging
from core.service import extract_domain_name

logger = logging.getLogger(__name__)
print logger.name

class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
        )

    def handle_noargs(self, **options):

        from core.models import Domain
        from core.views import search
        logger.info("custom command start running ")
        from django.test import Client
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        f = open("/tmp/domains.txt")
        data = f.readlines()

        for d in data:
            try:
                d = extract_domain_name(d)
                d = d.strip()
                domain = Domain.objects.all().filter(domain=d)
                if domain:
                    logger.info("%s has been found in system, skip" % d)
                    continue

                logger.info("start searching domain %s" % d)
                c.post("/search", {"domain":d})
            except Exception, e :
                logger.error("fucked up for domain %s" % d)
                logger.error(e)


        logger.info("done")

