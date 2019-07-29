from django.contrib.redirects.models import Redirect
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from ixxy_admin_utils.model_mixins import AdminUrlMixin


def url_to_link_html(url):
    return mark_safe('<a href="{}" title="{}">{}</a>'.format(url, url, truncatechars(url, 64)))


class Sentry404Issue(AdminUrlMixin, models.Model):
    
    url = models.URLField(max_length=2048)
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()
    sentry_id = models.PositiveIntegerField()
    
    @property
    def link_html(self):
        return url_to_link_html(self.url)
    
    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name = "404 Issue"


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
        return '{} on {}'.format(self.issue.url, self.date_created)
    
    class Meta:
        verbose_name = "404 Report"


class IgnoredUrl(AdminUrlMixin, models.Model):

    url = models.CharField(max_length=512)

    def __unicode__(self):
        return self.url


class RedirectFacade(AdminUrlMixin, Redirect):
    
    """Simplified Redirect proxy model to allow a nicer UI"""
    
    class Meta:
        verbose_name = "404 Redirect"
        proxy = True
