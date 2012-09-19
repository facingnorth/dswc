import logging
logger = logging.getLogger(__name__)

"""
check the site has been indexed by dmoz or not, return boolean True or False
"""
def dmoz_indexed(domain):
    logger.info("check domain %s has been indexed with dmoz" % domain)
    import urllib2
    from BeautifulSoup import BeautifulSoup
    #from http://stackoverflow.com/questions/802134/changing-user-agent-on-urllib2-urlopen
    url = "http://www.dmoz.org/search/?q={0}".format(domain)
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    result =soup.findAll("h3", {"class" : "open-dir-sites"})
    if result:
        return True

    return False