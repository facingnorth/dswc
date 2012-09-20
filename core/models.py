from datetime import datetime
from django.db import models

# Create your models here.
class Domain(models.Model):
    domain = models.CharField(max_length=255)
    ip = models.CharField(max_length=100)
    server = models.CharField(max_length=255, null=True)
    x_powered_by = models.CharField(max_length=255, null=True)
    cms = models.CharField(max_length=255, null=True)
    isp = models.CharField(max_length=255, null=True)
    country_code = models.CharField(max_length=255, null=True)
    country_name = models.CharField(max_length=255, null=True)
    region_name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)

    page_rank = models.IntegerField(null=True)
    alexa_rank = models.IntegerField(null=True)
    archived = models.DateTimeField(null=True)

    checked_at = models.DateTimeField(default=datetime.now())

    request_ip  = models.CharField(max_length=255, null=True)

    request_user_agent  = models.CharField(max_length=255, null=True)
    request_isp  = models.CharField(max_length=255, null=True)
    request_country_code  = models.CharField(max_length=255, null=True)
    request_country_name  = models.CharField(max_length=255, null=True)
    request_city  = models.CharField(max_length=255, null=True)
    request_region_name = models.CharField(max_length=255, null=True)
    request_latitude = models.CharField(max_length=255, null=True)
    request_longitude = models.CharField(max_length=255, null=True)
    request_referer = models.CharField(max_length=255, null=True)


    title = models.CharField(max_length=400, null=True)
    keywords = models.CharField(max_length=2550, null=True)
    description = models.CharField(max_length=2550, null=True)
    encoding = models.CharField( max_length=20,null=True)
    full_html = models.TextField()
    content = models.TextField()

    has_robots_txt = models.BooleanField()
    has_sitemap_xml = models.BooleanField()
    www_resolve = models.BooleanField()

    w3c_markup_errors = models.IntegerField()
    w3c_markup_warnings = models.IntegerField()
    w3c_css_errors = models.IntegerField()
    w3c_css_warnings =models.IntegerField()


    google_indexed=models.IntegerField()
    google_back_links =models.IntegerField()
    dmoz_indexed = models.BooleanField()


    has_conversion_form = models.NullBooleanField(null=True)
    num_of_js_files = models.IntegerField(null=True)
    using_google_analytics = models.NullBooleanField(null=True)


    def __unicode__(self):
        return self.domain


    def set_all_archived(self):
        from django.db import connection, transaction
        cursor = connection.cursor()

        # Data modifying operation - commit required
        cursor.execute("UPDATE core_domain SET archived = now() WHERE domain = %s and archived is NULL", [self.domain])
        transaction.commit_unless_managed()



class SeoImage(models.Model):
    src = models.CharField(max_length=400,null=True)
    alt = models.CharField(max_length=1000,null=True)
    title = models.CharField(max_length=1000,null=True)
    
    domain = models.ForeignKey(Domain)

    def alt_missing(self):
        return self.alt is None





class SeoHeading(models.Model):
    level = models.IntegerField()
    content = models.CharField(max_length=1000,null=True)
    domain = models.ForeignKey(Domain)

#class SeoLink(models.Model):
#    src = models.CharField(null=True)
#    title = models.ForeignKey(Domain)


class NameServer(models.Model):
    hostname = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    isp = models.CharField(max_length=255, null=True)
    domain = models.ForeignKey(Domain)


class MXServer(models.Model):
    hostname = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    isp = models.CharField(max_length=255, null=True)
    priority =  models.IntegerField()

    domain = models.ForeignKey(Domain)

class Redirection(models.Model):
    key = models.CharField(max_length=800, unique=True)
    short_url = models.CharField(max_length=800)

#class Person(models.Model):
#    first_name = models.CharField(max_length=30)
#    last_name = models.CharField(max_length=30)