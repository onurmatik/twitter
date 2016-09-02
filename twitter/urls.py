from django.conf.urls import url
from twitter.views import Authorize


urlpatterns = [
    url(r'^auth/$', Authorize.as_view(), name='authorize'),
]
