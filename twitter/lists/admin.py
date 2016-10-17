from django import forms
from django.contrib import admin
from django.conf import settings
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
        owner_screen_name, slug = None, None
        if self.cleaned_data['members']:
            # create a new Twitter list
            token = Token.objects.filter(data__screen_name=settings.TWITTER_DEFAULT_USER).first()
            if token:
                client = token.get_client()
                response = client.api.lists.create.post(
                    name=self.cleaned_data['name'],
                    mode=self.cleaned_data['mode'],
                )
                list_id = response.data['id']
                owner_screen_name, slug = response.data['user']['screen_name'], response.data['slug']
                members = self.cleaned_data['members']
                while len(members) > 0:
                    chunk = members[:100]
                    del(members[:100])
                    response = client.api.lists.members.create_all.post(
                        list_id=list_id,
                        screen_name=chunk,
                    )
        else:
            # URL; fetch an existing Twitter list
            owner_screen_name, x, slug = self.cleaned_data['name'].split('/')[-3:]

        # fetch and create the local list
        token = Token.objects.get_for_resource('/lists/show')
        if token and owner_screen_name and slug:
            client = token.get_client()
            response = client.api.lists.show.get(
                owner_screen_name=owner_screen_name,
                slug=slug,
            )
            return List(
                id=response.data['id'],
                data=response.data,
            )


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    search_fields = ('data', 'id')
    list_display = ('id', '__unicode__', 'updated', 'member_count', 'subscriber_count',)
    actions = ('update_members', 'update_subscribers',)

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            return ListForm
        else:
            return super(ListAdmin, self).get_form(request, obj, **kwargs)

    def update_members(self, request, queryset):
        for l in queryset:
            l.update_member_ids()

    def update_subscribers(self, request, queryset):
        for l in queryset:
            l.update_subscriber_ids()
