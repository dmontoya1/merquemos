from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html


class SoftDeletionModelAdminMixin(admin.ModelAdmin):
    """
    """

    exclude = ('deleted_at',)
    actions = None
    extra_list_display = ()
    
    def response_change(self, request, obj):
        """
        """

        opts = self.model._meta
        custom_redirect = False

        if "_soft-delete" in request.POST:
            obj.soft_delete() 
            custom_redirect = True

        if "_revive" in request.POST:
            obj.revive() 
            custom_redirect = True

        if custom_redirect:
            redirect_url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name))
            return HttpResponseRedirect(redirect_url)
        else:
             return super(SoftDeletionModelAdminMixin, self).response_change(request, obj)

    def is_alive(self, obj):
        """
        """

        icon = 'yes'
        if obj.deleted_at:
            icon = 'no'        
        return format_html(
            '<img src="/static/admin/img/icon-{icon}.svg" alt="{icon}">'.format(
                icon=icon
            )
        )

    def get_list_display(self, request):
        """
        """

        return self.extra_list_display + ('is_alive', )  
    
    def get_queryset(self, request):
        qs = super(SoftDeletionModelAdminMixin, self).get_queryset(request)
        return qs

            
    

    