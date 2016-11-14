from django.http import HttpResponseRedirect


class RedirectableAdmin(object):
    
    """If you use this as a mixin to your ModelAdmin then the change and add forms will accept
        a url parameter '_redirect' and redirect to that on save"""
    
    def response_post_save_change(self, request, obj):
        if '_redirect' in request.GET:
            return HttpResponseRedirect(request.GET['_redirect'])
        else:
            return super(RedirectableAdmin, self).response_post_save_change(request, obj)

    def response_post_save_add(self, request, obj):
        if '_redirect' in request.GET:
            return HttpResponseRedirect(request.GET['_redirect'])
        else:
            return super(RedirectableAdmin, self).response_post_save_add(request, obj)

    def delete_view(self, request, object_id, extra_context=None):
        response = super(RedirectableAdmin, self).delete_view(request, object_id, extra_context)
        if '_redirect' in request.GET and response.status_code == 302:
            return HttpResponseRedirect(request.GET['_redirect'])
        else:
            return response
