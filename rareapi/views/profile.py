"""View module for handling requests about user profiles"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import RareUser, Subscription, rareuser


class Profile(ViewSet):
    """User can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info
        """
        rareuser = RareUser.objects.get(user=request.auth.user)
        subscriptions = Subscription.objects.filter(subscribers=rareuser)

        subscriptions = SubscriptionsSerializer(
            subscriptions, many=True, context={'request': request})
        rareuser = RareUserSerializer(
            rareuser, many=False, context={'request': request})

        # Manually construct the JSON structure you want in the response
        profile = {}
        profile["rareuser"] = rareuser.data
        profile["subscriptions"] = subscriptions.data

        return Response(profile)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('user', 'bio', 'profile_image_url')


class SubscriptionsSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    class Meta:
        model = Subscription
        fields = ('id', 'game', 'description', 'date', 'time')