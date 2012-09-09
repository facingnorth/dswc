
def get_page_indexed(domain):
    import urllib2
    from BeautifulSoup import BeautifulSoup
    #from http://stackoverflow.com/questions/802134/changing-user-agent-on-urllib2-urlopen
    url = "https://www.google.com/search?q=%22{0}%22-site:{1}".format(domain,domain)
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()

    soup = BeautifulSoup(html)
    soup.prettify()
    result =soup.find("div",{"id": "resultStats"}).string
    print result
#    result = result.lower().replace("About ","")
#    result = result.replace(" results","")
    result = result.replace(',','')
    return result

print get_page_indexed("xhtmlweaver.com")