
"""URL Configuration"""

from rareapi.views.post import PostView
from rest_framework import routers
from rareapi.views import register_user, login_user
from django.conf.urls import include
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rareapi.views import TagView, PostView, SubscriptionsView, CommentView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tags', TagView, 'tag')
router.register(r'posts', PostView, 'post')
router.register(r'comments', CommentView, 'comment')
router.register(r'subscriptions', SubscriptionsView, 'subscription')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))]
