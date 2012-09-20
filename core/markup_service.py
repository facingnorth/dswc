from BeautifulSoup import BeautifulSoup
from collections import Counter
import logging
import re
import urllib2



logger = logging.getLogger(__name__)
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True



'''
check whether the domain has robots.txt
'''

def has_robots_txt(domain):
    import urllib2
    url = "http://{0}/robots.txt".format(domain)
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    request = urllib2.Request(url,None,headers)
    request.get_method = lambda : 'HEAD'

    try:
        response = urllib2.urlopen(request)
        if response.code==200:
            return True
    except urllib2.HTTPError ,e:
        logger.info(e)
        return False


def has_sitemap_xml(domain):
    import urllib2
    url = "http://{0}/sitemap.xml".format(domain)
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    request = urllib2.Request(url,None,headers)
    request.get_method = lambda : 'HEAD'

    try:
        response = urllib2.urlopen(request)

        if response.code==200:
            return True
    except urllib2.HTTPError ,e:
        logger.info(e)
        return False




class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp,
            code, msg,
            headers)
        result.status = code
        return result

    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp,
            code, msg,
            headers)
        result.status = code
        return result

#request = urllib2.Request("http://xhtmlweaver.com")
#opener = urllib2.build_opener(SmartRedirectHandler())
#obj = opener.open(request)
#print 'I capture the http redirect code:', obj.status
#print 'Its been redirected to:', obj.url


#
def www_resolve(domain):
    import urllib2
    url = "http://{0}".format(domain)
    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:13.0) Gecko/20100101 Firefox/13.0.1',
                'Host': domain
            }
    request = urllib2.Request(url,None,headers)
    response = None
    try:
        response = urllib2.urlopen(request)
        response.read()
        if response.code==200:
            return "No"
    except urllib2.HTTPError ,e:
        request = urllib2.Request("http://{0}".format(domain))
        opener = urllib2.build_opener(SmartRedirectHandler())
        obj = opener.open(request)

        if obj.status in (301, 302):
            return True
        else:
            return False




def extract_seo_facts(url):
    dict = {}
    #todo make sure it works for http and https
    url = "http://" + url
    logger.info("extracting seo facts for url %s" % url)
    page=urllib2.urlopen(url)
    
    source = page.read()

    dict['source'] = source
    soup = BeautifulSoup(source)
    soup.prettify()

    dict['title'] = str(soup.title.string) #get html page title
    dict['encoding'] = soup.declaredHTMLEncoding #get html page encoding

    #iterate through meta tags to find keywords and description
    metas = soup.findAll("meta")
    for m in metas:
        if m.get('name')=='keywords':
            dict['keywords'] = m.get('content')
        if m.get('name')=='description':
            dict['description'] = m.get('content')



    for i in range(6):
        if i is None:
            i=0
        heading_label = "h%s" % (i+1) ##start from h1
        headings = soup.findAll(heading_label)
        for h in headings:
            if dict.get(heading_label) is None:
                dict[heading_label] = list()
                dict[heading_label].append(h.string)
            else:
                dict[heading_label].append(h.string)


    dict['images']  = soup.findAll("img")


    forms = soup.findAll("form")
    if forms is not None and len(forms)>0:
        dict['has_conversion_form'] = True
    else:
        dict['has_conversion_form'] = False

    dict['num_of_js_files'] = 0
    scriptlets = soup.findAll("script")
    for script in scriptlets:
        if script.get("src") is not None:
            dict['num_of_js_files'] += 1
        else:
            if "_gaq.push" in script.text:
                dict['using_google_analytics'] = True


    #http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
    texts = soup.findAll(text=True)
    text_content = (str(filter(visible,texts)))

    dict['text_content'] =text_content

    return dict