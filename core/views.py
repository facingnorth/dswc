# Create your views here.
import datetime
import logging
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from core.markupservice import extract_seo_facts
from core.models import Domain, NameServer, SeoImage, SeoHeading
from service import *

NUMBER_OF_RECENT_SEARCH = 15

logger = logging.getLogger(__name__)

def is_domain_valid(d):
    if (d is None) or (len(d.strip())==0):
        return None
    try:
        return get_ip_from_domain(d)
    except :
        return None

def index(request):
    return render(request, 'index.html', {"recent_domains":get_latest_n_domain_checks(NUMBER_OF_RECENT_SEARCH)},)

def view(request, d):
    try:
        domain = Domain.objects.all().filter(archived__isnull=True).get(domain__exact=d)
    except :
        return search(request, d)


    return render(request, 'index.html', {"domain": domain, "view":True ,   "name_servers":domain.nameserver_set.all(),
                                          "mail_servers":domain.mxserver_set.all(),
                                          "recent_domains":get_random_domain_checks(NUMBER_OF_RECENT_SEARCH)})


def search(request, d=None):
    if d is None:
        d = request.REQUEST['domain'] #todo to lower

    d = extract_domain_name(d)
    ip = is_domain_valid(d)

    if ip is None:
        return render(request, 'index.html', {"error": "this is not valid site!"},)


    seo_dict=None
    headers = get_http_headers(d)
    print headers

    domain = Domain()
    domain.domain = d

    domain.set_all_archived() ##clean up all existing ones

    domain.ip = ip


    geo_record = get_geo_record(domain.ip)
    domain.city = geo_record['city']
    domain.state = geo_record.get("region_name")
    domain.country_code = geo_record['country_code']
    domain.longitude = geo_record['longitude']
    domain.latitude = geo_record['latitude']

    domain.isp = get_isp(domain.ip)
    domain.alexa_rank = get_alexa_rank(d)
    domain.page_rank = get_page_rank_rank(d)

    domain.request_ip = request.META['REMOTE_ADDR']

    domain.request_country_code = get_isp(domain.request_ip)

    client_geo_record = get_geo_record(domain.request_ip)
    domain.request_ip = request.META['REMOTE_ADDR']
    domain.request_user_agent  = request.META['HTTP_USER_AGENT']
    domain.request_referer = request.META.get('HTTP_REFERER')
    
    if client_geo_record is not None:
        domain.request_country_code =  client_geo_record['country_code']
        domain.request_city =  client_geo_record['city']
        domain.request_latitude =  client_geo_record['latitude']
        domain.request_longitude =  client_geo_record['longitude']

    domain.save()


    if headers is not None:
        #domain.server= get_header_value(headers, SERVER_KEY)
        #domain.x_powered_by= get_header_value(headers, X_POWERED_BY_KEY)
        seo_dict = extract_seo_facts(domain.domain)
        domain.title = seo_dict.get('title')
        domain.encoding = seo_dict.get('encoding')
        domain.keywords = seo_dict.get('keywords')
        domain.description = seo_dict.get('description')

        domain.full_html = seo_dict.get('source')
        domain.content = seo_dict.get('text_content')
        domain.save()

        if seo_dict.get("images"):
            for i in seo_dict.get("images"):
                image = SeoImage()
                image.src = i.get('src')
                image.alt = i.get('alt')
                image.title = i.get('title')
                image.domain = domain
                image.save()


        for i in range(6):
            if seo_dict.get("h%s" % i):
                for heading in seo_dict.get("h%s" % i ):
                    h = SeoHeading()
                    h.content = heading
                    h.level = i
                    h.domain = domain
                    h.save()

                    
    name_servers = get_ns_record(domain.domain)
    for v in name_servers:
        ns = NameServer()
        ns.hostname = v
        ns.ip = get_ip_from_domain(v)
        ns.isp = get_isp(ns.ip)
        ns.domain =domain
        ns.save()


    mail_servers = get_mx_record(domain.domain)
    print mail_servers
    for mx in mail_servers:
        mx.domain  = domain
        mx.save()



    return render(request, 'index.html', {"domain": domain, "name_servers":domain.nameserver_set.all(),
                                          "mail_servers":domain.mxserver_set.all(),
                                          "seo_dict": seo_dict,
                                          "recent_domains":get_latest_n_domain_checks(NUMBER_OF_RECENT_SEARCH)})
