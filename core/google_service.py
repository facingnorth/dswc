import logging
import urllib

logger = logging.getLogger(__name__)


def google_backlinks(domain):
    logger.info("begin google_backlinks for domain %s" % domain)
    import urllib2
    from BeautifulSoup import BeautifulSoup
    #from http://stackoverflow.com/questions/802134/changing-user-agent-on-urllib2-urlopen
    url = "https://www.google.com/search?q=%s".format(domain,domain)
    keyword = '"{0}" -site:{1}'.format(domain,domain)
    url = (url % urllib.quote_plus(keyword))
    logger.info(url)
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()

    soup = BeautifulSoup(html)
    soup.prettify()
    result =soup.find("div",{"id": "resultStats"}).string
    logger.info("Results %s" %  result)
    if result:
        if result=='1 result':
            return 1
        result = result.lower().replace("about ","")
        result = result.replace(" results","")
        result = result.replace(',','')
    else:
        result= 0

    logger.info("google_backlinks domain %s results %s" % (domain, result))
    return result

def google_indexed(domain):
    logger.info("begin google_indexed for domain %s" % domain)
    import urllib2
    from BeautifulSoup import BeautifulSoup
    #from http://stackoverflow.com/questions/802134/changing-user-agent-on-urllib2-urlopen
    url = "https://www.google.com/search?q=site:{1}".format(domain,domain)
    logger.info(url)
    headers = { 'User-Agent' : 'Mozilla/5.0'}
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    soup.prettify()
    result =soup.find("div",{"id": "resultStats"}).string
    logger.info("Results %s" %  result)
    if result:
        if result=='1 result':
            return 1
        result = result.lower().replace("about ","")
        result = result.replace(" results","")
        result = result.replace(',','')
    else:
        result= 0

    logger.info("google_indexed domain %s results %s" % (domain, result))
    return result