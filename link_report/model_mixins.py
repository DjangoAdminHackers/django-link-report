from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe


class AdminUrlMixin(object):
    @staticmethod
    def _get_admin_url_for_content_type(content_type, admin_url_name, args=None):
        return reverse(
            "admin:{}_{}_{}".format(
                content_type.app_label,
                content_type.model,
                admin_url_name,
            ),
            args=args or (),
        )
    
    @classmethod
    def _get_admin_url(cls, admin_url_name, args=None):
        content_type = ContentType.objects.get_for_model(cls, for_concrete_model=False)
        try:
            return cls._get_admin_url_for_content_type(content_type, admin_url_name, args)
        except NoReverseMatch:
            # We might not have a modeladmin for the proxy model so try the concrete model
            content_type = ContentType.objects.get_for_model(cls)
            return cls._get_admin_url_for_content_type(content_type, admin_url_name, args)
    
    @cached_property
    def changeform_url(self):
        return self._get_admin_url('change', args=(self.pk,))
    
    @cached_property
    def changelist_url(self):
        return self._get_admin_url('changelist')
    
    @classmethod
    def get_changelist_url(cls):  # We don't always have an instance
        return cls._get_admin_url('changelist')
    
    @classmethod
    def get_addform_url(cls):
        return cls._get_admin_url('add')
    
    def view_link(self):
        return mark_safe(
            u'<a href="{}" style="white-space: nowrap">View</a>'.format(self.get_absolute_url()))
    view_link.allow_tags = True
    view_link.short_description = ''
    
    def change_link(self, link_text='Edit', redirect=None):
        redirect_param = '?_redirect={}'.format(redirect) if redirect else ''
        return mark_safe(
            u'<a href="{}{}" class="changelink">{}</a>'.format(
                self.changeform_url,
                redirect_param,
                link_text,
            )
        )
    change_link.allow_tags = True
    change_link.short_description = ''
