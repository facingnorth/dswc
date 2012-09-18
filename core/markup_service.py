from BeautifulSoup import BeautifulSoup
from collections import Counter
import logging
import re
import urllib2

dict = {}

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
        print e
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
        print e
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
        print response.code
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
        headings = soup.findAll("h%s" % i)
        for h in headings:
            if dict.get('h%s' % i) is None:
                dict['h%s' % i] = []
            dict['h%s' % i] =dict['h%s' % i].append(h.string)


    dict['images']  = soup.findAll("img")

    #http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
    texts = soup.findAll(text=True)
    text_content = (str(filter(visible,texts)))

    dict['text_content'] =text_content

    return dict

    #top_words = Counter(text_content.split()).most_common(10)

    #for word, frequency in top_words:
    #    print("%s %d" % (word, frequency))

extract_seo_facts("www.netregistry.com.au")

#print soup.meta['http-equiv']
#
#/usr/bin/python /home/wtao/dswc/core/markup_service.py
#[u'DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"', u'\n', <html xmlns="http://www.w3.org/1999/xhtml">
#<head>
#<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
#<meta name="robots" content="index,follow" />
#<meta name="keywords" content="psd to html, psd to wordpress, wordpress, wordpress theme, wordpress development, css, xhtml, markup, table-less, html slicing, xhtml slicing, html production, xhtml production, semantic coding, table-less html, table-less xhtml, shorthand css, css, xhtml strict, xhtml transitional, convert design to html, convert psd to html, convert image to html, convert png to html, slice psd, convert psd to xhtml, convert image to xhtml, convert png to xhtml" />
#<meta name="description" content="XhtmlWeaver provides PSD to HTML and WordPress service, gives graphic designers and design agencies the ability to provide a full web design offering without having to learn any programming skills." />
#<meta name="google-site-verification" content="44hD87z5TCfLZORuxc4Y0whXru5A_eS4DnIRKHI8nnE" />
#<title>PSD to HTML | PSD to WordPress | Design to HTML  | XhtmlWeaver | Sydney, Australia</title>
#<script type="text/javascript" src="/scripts/googlewebfont.js"></script>