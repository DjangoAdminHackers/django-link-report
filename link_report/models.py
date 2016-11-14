from .model_mixins import AdminUrlMixin
from django.contrib.redirects.models import Redirect
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe


def url_to_link_html(url):
    return mark_safe('<a href="{}" title="{}">{}</a>'.format(url, url, truncatechars(url, 64)))


class Sentry404Issue(AdminUrlMixin, models.Model):
    
    url = models.URLField(max_length=2048)
    first_seen = models.DateTimeField()  # u'2016-03-21T22:34:26Z',
    last_seen = models.DateTimeField()  # u'2016-11-08T22:22:05Z',
    sentry_id = models.PositiveIntegerField()  # u'http://138.68.156.186/ixxy/lily/issues/5502/',
    
    @property
    def link_html(self):
        return url_to_link_html(self.url)
    
    def __unicode__(self):
        return self.url


class Sentry404Event(AdminUrlMixin, models.Model):
    
    issue = models.ForeignKey(Sentry404Issue, related_name='events')

    date_created = models.DateTimeField()
    sentry_id = models.PositiveIntegerField()
    referer = models.CharField(max_length=1024, null=True, blank=True)
    referer_domain = models.CharField(max_length=128, null=True, blank=True)
    user_agent = models.CharField(max_length=512, null=True, blank=True)
    
    browser = models.CharField(max_length=128, null=True, blank=True)
    browser_type = models.CharField(max_length=128, null=True, blank=True)
    device = models.CharField(max_length=128, null=True, blank=True)
    os = models.CharField(max_length=128, null=True, blank=True)
    user = models.CharField(max_length=128, null=True, blank=True)
    
    def __unicode__(self):
        return u'{} on {}'.format(self.issue.url, self.date_created)
    
    
class RedirectFacade(AdminUrlMixin, Redirect):
    
    """Simplified Redirect Model """
    
    class Meta:
        verbose_name = "Redirect"
        proxy = True
