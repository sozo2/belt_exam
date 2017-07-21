from django.conf.urls import url, include
from views import *

urlpatterns = [
    url(r'^$', index),
    url(r'register$', register_user),
    url(r'login$', login_user),
    url(r'quotes$', load_home),
    url(r'quote/new$', add_quote),
    url(r'favorite/(?P<quote_id>\d+)$', add_favorite),
    url(r'remove/(?P<favorite_id>\d+)$', remove_favorite),
    url(r'user/(?P<user_id>\d+)$', user_page),
    url(r'logout$', logout),
]