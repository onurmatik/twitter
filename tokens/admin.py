from django.contrib import admin
from tokens.models import Application, Token


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'permission')


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'app', 'valid')
    list_editable = ('app',)
