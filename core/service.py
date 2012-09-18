import logging
from random import randint
from django.db.models.aggregates import Max, Count
from pygeoip import GeoIP
import pygeoip
from core.models import Domain, MXServer
from settings import GEO_ISP_FILE, GEO_LITE_CITY_FILE

logger = logging.getLogger(__name__)

X_POWERED_BY_KEY = "x-powered-by"
SERVER_KEY = "server"


def extract_domain_name(d):
    d = d.lower()
    if d.startswith("http://"):
        d= d[7:]
    if d.startswith("https://"):
        d= d[8:]

    d= d.split("/")[0]
    return d


def get_ns_record(domain):
    name_servers = []
    import dns.resolver
    try:
        answers = dns.resolver.query(domain, 'NS')
        for rdata in answers:
            name_servers.append(str(rdata))
    except Exception, e:
        logger.error("error to get ns record for domain %s" % domain)
        logger.error(e)


    return name_servers

def get_mx_record(domain):
    mail_servers = []
    import dns.resolver
    try:
        answers = dns.resolver.query(domain, 'MX')
        for rdata in answers:
            mx = MXServer()
            mx.hostname= rdata.exchange
            mx.ip = get_ip_from_domain( str(mx.hostname)[0:-1])
            mx.isp = get_isp(mx.ip)
            mx.priority = rdata.preference
            mail_servers.append(mx)
    except Exception, e:
        logger.error("error to get MX record for domain %s" % domain)
        logger.error(e)
    return mail_servers





def get_ip_from_domain(domain):
    import socket
    return socket.gethostbyname(domain)


def get_isp(ip):
    gi = GeoIP(GEO_ISP_FILE ,pygeoip.STANDARD )
    isp = gi.org_by_addr(ip)
    if isp is  None:
        isp = "Unknown"
    return isp

#{'city': u'Ryde', 'region_name': u'02', 'time_zone': 'Australia/NSW', 'longitude': 151.10000000000002, 'metro_code': '', 'country_code3': 'AUS', 'latitude': -33.8167, 'postal_code': None, 'country_code': 'AU', 'country_name': 'Australia'}
def get_geo_record(ip):
    gi = GeoIP(GEO_LITE_CITY_FILE, pygeoip.STANDARD )
    x =  gi.record_by_addr(ip)
    return x


def get_alexa_rank(domain):
    from core.rank_provider import AlexaTrafficRank
    return AlexaTrafficRank().get_rank(domain)

def get_page_rank_rank(domain):
    from core.rank_provider import GooglePageRank
    return GooglePageRank().get_rank(domain)


def get_http_headers(domain):
    import httplib
    conn = httplib.HTTPConnection(domain)
    conn.timeout =30
    try:
        conn.request("HEAD", "/")
        res = conn.getresponse()
        status = str(res.status)
        if status.startswith("2") or status.startswith("3"):  #2xx or #3xx is OK response
            return res.getheaders()
        return None
    except Exception, e:
        logger.error("error to http headers for domain %s" % domain)
        logger.error(e)
        return None




def get_header_value(headers, key):
    if headers is None:
        return None
    ##this returns a tuple and has two elements {'server', 'nginx/xxx'}
    for h in headers:
        if key in  h:
            return h[1]


def get_latest_n_domain_checks(number):
    return Domain.objects.all().filter(archived__isnull=True).order_by('-checked_at')[:number]

TIMES=15
def using_max(model, TIMES=15):
    max_ = model.objects.aggregate(Max('id'))['id__max']
    total_ = model.objects.aggregate(Count('id'))

    if TIMES>total_:
        TIMES = total_

    i=0
    while i < TIMES:
       try:
           yield model.objects.filter(archived__isnull=True).get(pk=randint(1, max_)).pk
           i += 1
       except model.DoesNotExist:
           pass

def get_random_domain_checks(number):
    domain_ids  = list(using_max(Domain,number))
    return Domain.objects.all().filter(pk__in=domain_ids)
