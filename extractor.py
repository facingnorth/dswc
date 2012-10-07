'''
extract records from alexa 1m file,
Criteria 1. ends with .au 2. hosted within australia
'''
from pygeoip import GeoIP

import os
import pygeoip

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

GEO_ISP_FILE = os.path.join(SITE_ROOT,"geoip/GeoIPISP.dat")
GEO_LITE_CITY_FILE = os.path.join(SITE_ROOT, "geoip/GeoLiteCity.dat")



def get_ip_from_domain(domain):
    import socket
    print "[%s]" % domain
    return socket.gethostbyname(domain)



#{'city': u'Ryde', 'region_name': u'02', 'time_zone': 'Australia/NSW', 'longitude': 151.10000000000002, 'metro_code': '', 'country_code3': 'AUS', 'latitude': -33.8167, 'postal_code': None, 'country_code': 'AU', 'country_name': 'Australia'}
def get_geo_record(ip):
    gi = GeoIP(GEO_LITE_CITY_FILE, pygeoip.STANDARD )
    x =  gi.record_by_addr(ip)
    return x

def is_au_domain(domain):


    if domain.endswith(".au"):
        print  domain

        return domain
#    else:
#        try:
#            if domain.endswith(".com"):
#                ip =get_ip_from_domain(domain)
#                info_map = get_geo_record(ip)
#                print info_map.get("country_code").lower()
#                if info_map.get("country_code").lower() =="au":
#                    return domain
#        except Exception,e:
#            return None
    return None


import logging
logger = logging.getLogger('script')
hdlr = logging.FileHandler(SITE_ROOT + "/log/top1m.log")
formatter = logging.Formatter('%(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


path =  os.path.join(SITE_ROOT,"data")
file =  os.path.join(path,"top-1m.csv")


f = open(file)

data = f.readlines()
for line in data:
    line = line.strip()
    values = line.split(",")
    number = int(values[0])
    domain = values[1]
    if number>500000:
        domain = is_au_domain(domain)
        if domain:
            logger.info(domain)