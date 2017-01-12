from django.contrib.admin import SimpleListFilter
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
