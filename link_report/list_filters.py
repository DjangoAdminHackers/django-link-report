from django.contrib.admin import SimpleListFilter
from django.contrib.redirects.models import Redirect
from link_report import link_report_settings

from .models import Sentry404Event


class UrlListFilter(SimpleListFilter):
    
    title = 'Internal or External Source?'
    parameter_name = 'is_internal'
    
    def lookups(self, request, model_admin):
        return (
            ('0', 'Internal'),
            ('1', 'External'),
        )
    
    def queryset(self, request, queryset):
        
        if self.value():
            if self.value() == '0':
                internal = Sentry404Event.objects.filter(referer__icontains=link_report_settings.BASE_URL)
                return queryset.filter(events=internal)
            elif self.value() == '1':
                assert isinstance(link_report_settings.BASE_URL, object)
                external = Sentry404Event.objects.exclude(referer__icontains=link_report_settings.BASE_URL)
                return queryset.filter(events=external)
        return queryset


class RedirectedListFilter(SimpleListFilter):
    title = 'Redirected?'
    parameter_name = 'redirected'
    
    def lookups(self, request, model_admin):
        return (
            ('0', 'No'),
            ('1', 'Yes'),
        )
    
    def queryset(self, request, queryset):
        
        if self.value():
            if self.value() == '0':
                return queryset.exclude(url__in=Redirect.objects.all().values_list('old_path', flat=True))
            elif self.value() == '1':
                return queryset.filter(
                    url__in=Redirect.objects.all().values_list('old_path', flat=True))
        return queryset