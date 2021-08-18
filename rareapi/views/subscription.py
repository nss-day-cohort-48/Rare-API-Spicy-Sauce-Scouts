"""View module for handling requests about subscriptions"""
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Subscription


class SubscriptionsView(ViewSet):
    """Rare subscriptions"""

    def create(self, request):
        """Handle POST operations for subscriptions

        Returns:
            Response -- JSON serialized subscriptions 
        """
        subscription = Subscription()
        subscription.follower = request.auth.user
        subscription.author = request.data["authorId"]
        subscription.created_on = request.data["created_on"]

        try:
            subscription.save()
            serializer = subscriptionSerializer(subscription, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single subscription

        Returns:
            Response -- JSON serialized subscription
        """
        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = subscriptionSerializer(subscription, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponseServerError()

    def update(self, request, pk=None):
        """Handle PUT requests for an event
        Returns:
            Response -- Empty body with 204 status code
        """
        subscription = Subscription.objects.get(pk=pk)
        subscription.follower = request.auth.user
        subscription.author = request.data["authorId"]
        subscription.created_on = request.data["created_on"]

        subscription.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests to subscriptions resource

        Returns:
            Response -- JSON serialized list of subscriptions
        """
        subscriptions = Subscription.objects.filter(follower = request.auth.user.id)

        # Support filtering subscriptions by label

        serializer = subscriptionSerializer(
            subscriptions, many=True, context={'request': request})
        return Response(serializer.data)


class subscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for subscriptions"""
    class Meta:
        model = Subscription
        fields = ('id', 'follower', 'author', 'created_on', 'ended_on')
