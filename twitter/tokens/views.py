from delorean import parse, epoch
from django.views.generic import RedirectView
from django.contrib.auth import login
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from twitter.api import UserClient
from twitter.tokens.models import Token, User


def wait(e):
    sleep_time = (epoch(int(e.headers['x-rate-limit-reset'])).datetime - parse(e.headers['date']).datetime).seconds + 1
    return sleep_time


class Authorize(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            # user is already authenticated
            return getattr(settings, 'LOGIN_REDIRECT_URL', '/')

        elif not set(self.request.GET.keys()).intersection(['oauth_callback_confirmed', 'oauth_verifier']):
            # first step: redirect to Twitter auth URL
            client = UserClient(
                settings.CONSUMER_KEY,
                settings.CONSUMER_SECRET,
            )
            token = client.get_signin_token(
                callback_url=settings.CALLBACK_URL
            )
            self.request.session['temp_token'] = token.oauth_token
            self.request.session['temp_token_secret'] = token.oauth_token_secret
            return token.auth_url

        elif self.request.GET.get('oauth_callback_confirmed') and self.request.GET.get('oauth_callback_confirmed') != 'true':
            # user did not authorize the app
            messages.add_message(
                self.request,
                messages.WARNING,
                "<b>C'mon!</b>"
            )

        elif self.request.GET.get('oauth_verifier'):
            # user authorized the app
            client = UserClient(
                settings.CONSUMER_KEY,
                settings.CONSUMER_SECRET,
                self.request.session['temp_token'],
                self.request.session['temp_token_secret'],
            )
            token = client.get_access_token(self.request.GET.get('oauth_verifier'))
            user, created = User.objects.get_or_create(
                username=token['screen_name'],
            )
            if created:
                Token.objects.create(
                    user=user,
                    data=token,
                )
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)
            if getattr(settings, 'LOGIN_REDIRECT_URL'):
                return reverse(getattr(settings, 'LOGIN_REDIRECT_URL'))
            else:
                return '/'
