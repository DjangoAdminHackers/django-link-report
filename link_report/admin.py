import link_report_settings
from datetime import timedelta
from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.db.models import Count
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from ixxy_admin_utils.admin_mixins import RedirectableAdmin
from ixxy_admin_utils.list_filters import makeRangeFieldListFilter
from .list_filters import UrlListFilter, RedirectedListFilter
from .models import Sentry404Issue, Sentry404Event, RedirectFacade


customDateRangeFilter = makeRangeFieldListFilter([
    ('Last 7 days', timedelta(days=-7), timedelta(days=0)),
    ('Last 30 days', timedelta(days=-30), timedelta(days=0)),
    ('Last 60 days', timedelta(days=-60), timedelta(days=0)),
])


@admin.register(Sentry404Issue)
class Sentry404IssueAdmin(admin.ModelAdmin):
    list_display = ['url', 'first_seen', 'last_seen', 'display_events', 'display_redirect']
    list_filter = [
        UrlListFilter,
        RedirectedListFilter,
        ('first_seen', customDateRangeFilter),
        ('last_seen', customDateRangeFilter),
    ]
    search_fields = ('url',)
    
    def get_queryset(self, request):
        qs = super(Sentry404IssueAdmin, self).get_queryset(request)
        return qs.annotate(event_count=Count('events'))
    
    def display_events(self, obj):
        event_list = obj.events.all().values_list('referer', 'date_created', 'browser_type')
        sources = {}
        for item in event_list:
            source_name = item[0] or '(None)'
            if source_name in sources:
                sources[source_name]['count'] += 1
                sources[source_name]['date_created'] == max(
                    sources[source_name]['date_created'], item[1]
                )
            else:
                sources[source_name] = {'count': 1, 'date_created': item[1]}
        html = mark_safe(u"""
            <table>
            <thead>
                <tr>
                    <td>Last seen</td><td>Count</td><td>Source</td>
                </tr>
            </thead>""")
        html += mark_safe(
            u''.join(
                [
                    u'<tr><td>{}<td>{}</td><td>{}</td></tr>'.format(
                        sources[x]['date_created'].strftime('%e/%m/%y'),
                        sources[x]['count'],
                        truncatechars(x, 64),
                    )
                    for x in sorted(sources.iterkeys())
                ]
            )
        )
        html += mark_safe(u'</table>')
        html += u'<strong>(<a href="{}">{} clicks from {} sources</a>)</strong>'.format(
            Sentry404Event.get_changelist_url() + '?issue__id__exact={}'.format(obj.pk),
            len(event_list),
            len(sources),
        )
        return html
    
    display_events.allow_tags = True
    display_events.short_description = 'Linked From'
    display_events.admin_order_field = 'event_count'
    
    def display_redirect(self, obj):
        old_path = obj.url.replace(link_report_settings.BASE_URL, '/')
        try:
            redirect = RedirectFacade.objects.get(old_path=old_path)
            return mark_safe(
                u'<a href="{0}">{0}</a>'.format(redirect.new_path)
            )
        except RedirectFacade.DoesNotExist:
            add_form_url = RedirectFacade.get_addform_url()
            return mark_safe(
                u'<a href="{}?site={}&old_path={}&_redirect={}">Add a redirect</a>'.format(
                    add_form_url,
                    Site.objects.first().pk,
                    old_path,
                    obj.changelist_url,
                )
            )
    
    display_redirect.allow_tags = True
    display_redirect.short_description = ''


@admin.register(Sentry404Event)
class Sentry404EventAdmin(admin.ModelAdmin):
    
    list_display = [
        'display_url',
        'browser_type',
        'device',
        'os',
        'user',
        'user_agent',
        'referer',
        'date_created',
    ]
    list_filter = [
        'date_created',
        'browser_type',
        'device',
        'os',
        'user',
        'referer_domain',
        'issue',
    ]
    search_fields = ['referer', 'user_agent', 'browser', 'device', 'os', 'user']
    readonly_fields = ['issue']
    
    def display_url(self, obj):
        return obj.issue.url
    
    display_url.allow_tags = True
    display_url.short_description = 'Url'


@admin.register(RedirectFacade)
class RedirectFacadeAdmin(RedirectableAdmin, admin.ModelAdmin):
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        
        if db_field.name in ['site', 'old_path']:
            kwargs['widget'] = forms.HiddenInput
        return super(RedirectFacadeAdmin, self).formfield_for_dbfield(db_field, **kwargs)
