import urllib
import urllib2

import logging
logger = logging.getLogger(__name__)


def w3c_markup_check(domain):
    URL = "http://validator.w3.org/check?uri=%s"
    SITE_URL = "http://{0}".format(domain)
    # pattern for HEAD request taken from
    # http://stackoverflow.com/questions/4421170/python-head-request-with-urllib2
    logger.info("URL is %s" % URL % urllib.quote(SITE_URL) )
    request = urllib2.Request(URL % urllib.quote(SITE_URL))
    request.get_method = lambda : 'HEAD'
    response = urllib2.urlopen(request)

    result = {'X-W3C-Validator-Errors':0, 'X-W3C-Validator-Warnings':0, 'valid':False }

    valid = response.info().getheader('X-W3C-Validator-Status')
    if valid == "Valid":
        result['valid'] =  True
    else:
        result['valid'] =  False

    result['X-W3C-Validator-Errors'] =   int(response.info().getheader('X-W3C-Validator-Errors'))
    result['X-W3C-Validator-Warnings'] =   int(response.info().getheader('X-W3C-Validator-Warnings'))

    return result


#todo merge into one method
def w3c_css_check(domain):
    URL =  "http://jigsaw.w3.org/css-validator/validator?uri=%s"
    SITE_URL = "http://{0}".format(domain)
    # pattern for HEAD request taken from
    # http://stackoverflow.com/questions/4421170/python-head-request-with-urllib2
    logger.info("URL is %s" % URL % urllib.quote(SITE_URL) )

    request = urllib2.Request(URL % urllib.quote(SITE_URL))
    request.get_method = lambda : 'HEAD'
    response = urllib2.urlopen(request)

    result = {}
    result = {'X-W3C-Validator-Errors':0, 'X-W3C-Validator-Warnings':0, 'valid':False }
    valid = response.info().getheader('X-W3C-Validator-Status')
    if valid == "Valid":
        result['valid'] =  True
    else:
        result['valid'] =  False

    result['X-W3C-Validator-Errors'] =   int(response.info().getheader('X-W3C-Validator-Errors'))


    return result