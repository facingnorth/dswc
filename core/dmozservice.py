
def get_page_indexed(domain):
    import urllib2
    from BeautifulSoup import BeautifulSoup
    #from http://stackoverflow.com/questions/802134/changing-user-agent-on-urllib2-urlopen
    url = "http://www.dmoz.org/search/?q={0}".format(domain)
    print url
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()

    soup = BeautifulSoup(html)
    
    #http://scrapy.org/
    result =soup.findAll("h3")
    print result
#    
    return result

print get_page_indexed("xhtmlweaver.com")