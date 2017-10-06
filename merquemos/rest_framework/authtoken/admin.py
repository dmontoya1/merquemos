from django.contrib import admin

from rest_framework.authtoken.models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)
    icon = '<i class="material-icons">devices_other</i>'
admin.site.register(Token, TokenAdmin)
