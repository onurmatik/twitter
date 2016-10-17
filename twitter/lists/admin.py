from django import forms
from django.contrib import admin
from django.conf import settings
from twitter.api import AppClient
from twitter.lists.models import List
from twitter.tokens.models import Token


class ListForm(forms.ModelForm):
    name = forms.CharField(required=False)
    members = forms.CharField(required=False, widget=forms.Textarea)
    mode = forms.ChoiceField(choices=(('public', 'public'), ('private', 'private')))

    class Meta:
        model = List
        fields = ['name', 'members', 'mode']

    def save(self, **kwargs):
        if self.members:
            # create a new Twitter list
            client = AppClient(
                consumer_key=settings.CONSUMER_KEY,
                consumer_secret=settings.CONSUMER_SECRET,
            )
            response = client.api.lists.create.post(
                name=self.name,
                mode=self.mode,
            )
            list_id = response.data['id']
            while len(self.members) > 0:
                members = self.members[:100]
                del(self.members[:100])
                response = client.api.lists.members.create_all.post(
                    list_id=list_id,
                    screen_name=members,
                )
        else:
            # URL; fetch an existing Twitter list
            owner_screen_name, x, slug = self.name.split('/')[-3:]
            token = Token.objects.get_for_resource('/lists/show')
            if token:
                client = token.get_client()
                response = client.api.lists.show(
                    owner_screen_name=owner_screen_name,
                    slug=slug,
                )
                List.objects.create(
                    id=response.data['id'],
                    data=response.data,
                )


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    search_fields = ('data', 'id')
    list_display = ('id', '__unicode__', 'updated', 'member_count', 'subscriber_count',)
    actions = ('update_members', 'update_subscribers',)
    form = ListForm

    def update_members(self, request, queryset):
        for l in queryset:
            l.update_member_ids()

    def update_subscribers(self, request, queryset):
        for l in queryset:
            l.update_subscriber_ids()
