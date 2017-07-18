from django.contrib import admin
from rest_framework_api_key.admin import ApiKeyAdmin
from rest_framework_api_key.models import APIKey

class CustomApiTokenAdmin(ApiKeyAdmin):

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def key_message(self, obj):
        if obj.key:
            return obj.key
        return "The API Key will be generated once you click save."

admin.site.unregister(APIKey)
admin.site.register(APIKey, CustomApiTokenAdmin)