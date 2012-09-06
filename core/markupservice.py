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


def extract_seo_facts(url):

    #todo make sure it works for http and https
    url = "http://" + url
    logger.info("extracting seo facts for url %s" % url)
    print ("extracting seo facts for url %s" % url)
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
            dict['h%s' % i] = h.string

    dict['images']  = soup.findAll("img")

    #http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
    texts = soup.findAll(text=True)
    text_content = (str(filter(visible,texts)))

    dict['text_content'] =text_content

    return dict

    #top_words = Counter(text_content.split()).most_common(10)

    #for word, frequency in top_words:
    #    print("%s %d" % (word, frequency))


#print soup.meta['http-equiv']
#
#/usr/bin/python /home/wtao/dswc/core/markupservice.py
#[u'DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"', u'\n', <html xmlns="http://www.w3.org/1999/xhtml">
#<head>
#<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
#<meta name="robots" content="index,follow" />
#<meta name="keywords" content="psd to html, psd to wordpress, wordpress, wordpress theme, wordpress development, css, xhtml, markup, table-less, html slicing, xhtml slicing, html production, xhtml production, semantic coding, table-less html, table-less xhtml, shorthand css, css, xhtml strict, xhtml transitional, convert design to html, convert psd to html, convert image to html, convert png to html, slice psd, convert psd to xhtml, convert image to xhtml, convert png to xhtml" />
#<meta name="description" content="XhtmlWeaver provides PSD to HTML and WordPress service, gives graphic designers and design agencies the ability to provide a full web design offering without having to learn any programming skills." />
#<meta name="google-site-verification" content="44hD87z5TCfLZORuxc4Y0whXru5A_eS4DnIRKHI8nnE" />
#<title>PSD to HTML | PSD to WordPress | Design to HTML  | XhtmlWeaver | Sydney, Australia</title>
#<script type="text/javascript" src="/scripts/googlewebfont.js"></script>