from django.contrib import admin
from twitter.tokens.models import Application, Token


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'permission')


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'app', 'valid')
    list_editable = ('app',)
    list_filter = ('valid',)
    search_fields = ('data',)
    actions = ('verify',)

    def verify(self, request, queryset):
        for token in queryset:
            if token.valid:
                token.verify()
