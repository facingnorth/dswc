#
#
##to get all dns records
#import pygeoip
#from pygeoip import  GeoIP
##
#def get_http_headers(domain):
#    import httplib
#    conn = httplib.HTTPConnection(domain)
#    conn.request("HEAD", "/")
#    res = conn.getresponse()
#    print type(res.status)
#
#    return res.getheaders()
#
#
#def get_server(headers):
#    for h in headers:
#        if "server" in  h:
#            print h[1]
#
#headers = get_http_headers("test.com.au")
#print headers
#
#
#
##
##
#def get_mx_record(domain):
#    import dns.resolver
#    answers = dns.resolver.query(domain, 'MX')
#    for rdata in answers:
#       print rdata
#
#
#print get_mx_record("xhtmlweaver.com")
#
#
##get_http_headers("reallyusefulcrew.com.au")
##get_mx_record("reallyusefulcrew.com.au")
##
##
##print get_pagerank("netregistruy.com.au")
#
#
#
##gi = GeoIP('/home/wtao/Desktop/GeoIPISP.dat', pygeoip.STANDARD )
##print gi
##
##x =  gi.org_by_name("xhtdsfasdfmlweaver.com")
###y = gi.country_code_by_addr("173.255.192.79")
##print x
###print y
#
#gi = GeoIP('/home/wtao/Desktop/GeoLiteCity.dat', pygeoip.STANDARD )
#print gi
#
##x =  gi.country_code_by_addr("173.255.192.79")
#x =  gi.record_by_addr("203.26.27.38")
#print x
##y = gi.country_code_by_addr("173.255.192.79")
#
#
#
#
##print socket.gethostbyaddr("69.163.221.122")
##
##
##print socket.gethostbyname('reallyusefulcrewasdfadsfa.com.au')
##
##
#
##>>> res = conn.getresponse()
##>>> print res.status, res.reason
##200 OK
##>>> print res.getheaders()
##[('content-length', '0'), ('expires', '-1'), ('server', 'gws'), ('cache-control', 'private, max-age=0'), ('date', 'Sat, 20 Sep 2008 06:43:36 GMT'), ('content-type', 'text/html; charset=ISO-8859-1')
#
#
#d = "http://www.g.com"
#d = d.lower()
#if d.startswith("http://"):
#    d= d[7:]
#if d.startswith("https://"):
#    d= d[8:]
#
#print d
#

