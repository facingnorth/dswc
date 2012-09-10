import urllib
import urllib2

URL = "http://validator.w3.org/check?uri=%s"
SITE_URL = "http://www.netregistry.com.au"

# pattern for HEAD request taken from
# http://stackoverflow.com/questions/4421170/python-head-request-with-urllib2

request = urllib2.Request(URL % urllib.quote(SITE_URL))
request.get_method = lambda : 'HEAD'
response = urllib2.urlopen(request)

valid = response.info().getheader('X-W3C-Validator-Status')
if valid == "Valid":
    valid = True
else:
    valid = False
errors = int(response.info().getheader('X-W3C-Validator-Errors'))
warnings = int(response.info().getheader('X-W3C-Validator-Warnings'))

print "Valid markup: %s (Errors: %i, Warnings: %i) " % (valid, errors, warnings)