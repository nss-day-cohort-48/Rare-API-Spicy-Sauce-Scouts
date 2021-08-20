"""View module for handling requests about user profiles"""
from django.contrib.auth.models import User
from django.http.response import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import RareUser, Post


class AuthorView(ViewSet):
    """User can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info
        """
        rareusers = RareUser.objects.all()

        serializer = RareUserSerializer(
            rareusers, many=True, context={'request': request})

            # Manually construct the JSON structure you want in the response
        return Response(serializer.data)

    def retrieve (self, request, pk=None):
        """Handle GET requests to single profile

        Returns:
            Response -- JSON representation of user info
        """
        try:

            rareuser = RareUser.objects.get(pk=pk)

            rareuser = RareUserSerializer(
            rareuser, many=False, context={'request': request})

            # Manually construct the JSON structure you want in the response
            profile = {}
            profile["rareuser"] = rareuser.data

            return Response(profile)

        except Exception as ex:
            return HttpResponseServerError(ex)


# class PostSerializer(serializers.ModelSerializer):
#     """JSON serializer for posts
#     Arguments:
#         serializer type
#     """
#     class Meta:
#         model = Post
#         fields = ('id', 'title', 'content', 'publication_date',
#                   'image_url', 'approved', 'category', 'tags', 'user')
        

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for rareUser's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers"""
    user = UserSerializer(many=False)
    # posts = PostSerializer(many=True)

    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url', 'post_set')
        depth = 1



