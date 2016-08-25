from twitter.models import Token
from twitter.api import TwitterRateLimitError, TwitterAuthError, TwitterClientError
from aura.users.models import TwitterUser
from time import sleep


TWITTER_LIST_OWNER, TWITTER_LIST_SLUG = 'abc', 'def'


# check tokens
tokens = Token.objects.filter(valid=True)
for token in tokens:
    token.verify()
tokens = Token.objects.filter(valid=True)


# get the member ids
client = tokens.first().get_client()
response = client.api.lists.members.get(
    owner_screen_name=TWITTER_LIST_OWNER,
    slug=TWITTER_LIST_SLUG,
    count=5000,
    include_entities=False,
    skip_status=True,
)
members = [user['id'] for user in response.data['users']]


def create_member_users():
    tokens = list(Token.objects.all())
    token = tokens.pop()
    uid = members.pop()
    while uid:
        u, created = TwitterUser.objects.get_or_create(id=uid)
        if created:
            u.update_details(client=client)
            u.get_mutuals(client=client)



tokens = list(Token.objects.all())
token = tokens.pop()
uid = members.pop()
while uid:
    print 'token: %s; user: %s' % (token.user, uid)
    user, created = TwitterUser.objects.get_or_create(id=uid)
    print user.name
    client = token.get_client()
    if created or not user.name or (not user.friend_ids and not user.protected):
        try:
            user.update_details(client)
            print 'getting connections for: %s' % user
            response = client.api.friends.ids.get(
                user_id=uid,
                count=5000,
            )
        except TwitterRateLimitError, e:
            try:
                token = tokens.pop()
            except IndexError:
                # no token available; sleep for a while
                print 'sleeping'
                sleep(900)
                tokens = list(Token.objects.all())
                token = tokens.pop()
            else:
                # put the id back and try with a different token next time
                twitter_user_ids.append(uid)
        except TwitterAuthError:
            print 'protected'
            user.protected = True
            user.save()
        except TwitterClientError:
            print 'deactivated'
            user.deactivated = True
            user.save()
        else:
            user.friend_ids = response.data.ids
            user.save()
    uid = twitter_user_ids.pop()
