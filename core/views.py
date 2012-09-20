# Create your views here.
import logging
from django.shortcuts import render
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


# the ip must be resolvable and site must be accssible at the time
def search(request, d=None):
    if d is None:
        d = request.REQUEST.get('domain') #todo to lower
        if d is None:
            return render(request, 'index.html', {"error": "domain name cannot be empty"},)


    d = extract_domain_name(d)
    ip = is_domain_valid(d)

    if ip is None:
        return render(request, 'index.html', {"error": "domain name is invalid"},)

    headers = get_http_headers(d) ##check whether the site is up

    if headers is None:
        return render(request, 'index.html', {"error": "website is down"},)

    seo_dict=None

    domain = Domain()
    domain.domain = d
    domain.set_all_archived() ##clean up all existing ones
    domain.ip = ip


    geo_record = get_geo_record(domain.ip)
    domain.city = geo_record['city']
    domain.region_name = geo_record.get("region_name")
    domain.country_code = geo_record['country_code']
    domain.country_name = geo_record['country_name']
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
        domain.request_country_name =  client_geo_record['country_name']
        domain.request_region_name =  client_geo_record['region_name']
        domain.request_city =  client_geo_record['city']
        domain.request_latitude =  client_geo_record['latitude']
        domain.request_longitude =  client_geo_record['longitude']


    from core.dmoz_service import dmoz_indexed
    domain.dmoz_indexed = dmoz_indexed(domain.domain)

    from core.markup_service import *
    domain.has_robots_txt = has_robots_txt(domain.domain)
    domain.has_sitemap_xml = has_sitemap_xml(domain.domain)
    domain.www_resolve = www_resolve(domain.domain)


    import core.w3c_service
    domain.w3c_markup_errors = core.w3c_service.w3c_markup_check(domain.domain)['X-W3C-Validator-Errors']
    domain.w3c_markup_warnings = core.w3c_service.w3c_markup_check(domain.domain)['X-W3C-Validator-Warnings']

    domain.w3c_css_errors = core.w3c_service.w3c_css_check(domain.domain)['X-W3C-Validator-Errors']
    domain.w3c_css_warnings = core.w3c_service.w3c_css_check(domain.domain)['X-W3C-Validator-Warnings']


    import core.google_service
    domain.google_back_links= core.google_service.google_backlinks(domain.domain)
    domain.google_indexed= core.google_service.google_indexed(domain.domain)



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

        domain.has_conversion_form = seo_dict.get("has_conversion_form")
        domain.num_of_js_files = seo_dict.get("num_of_js_files")
        domain.using_google_analytics = seo_dict.get("using_google_analytics")


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
                    print "heading" + heading
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
    for mx in mail_servers:
        mx.domain  = domain
        mx.save()


    mx_servers = domain.mxserver_set.all(),
    name_servers = domain.nameserver_set.all()
    images = domain.seoimage_set.all()


    return render(request, 'index.html', {"domain": domain, "name_servers": name_servers,
                                          "mail_servers": mail_servers,
                                          "images": images,
                                          "seo_dict": seo_dict,
                                          "recent_domains":get_latest_n_domain_checks(NUMBER_OF_RECENT_SEARCH)})