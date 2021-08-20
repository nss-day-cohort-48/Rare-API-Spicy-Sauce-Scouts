"""View module for handling requests about comments"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comment,Post,RareUser
from datetime import date

class CommentView(ViewSet):
    """Rare comments"""

    def create(self, request):
        """Handle POST operations for comments

        Returns:
            Response -- JSON serialized comments 
        """
        comment = Comment()
        comment.post = Post.objects.get(pk=request.data['post'])
        comment.author =  RareUser.objects.get(user=request.auth.user)
        comment.content = request.data["content"]
        comment.created_on = date.today()


        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment

        Returns:
            Response -- JSON serialized comment
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponseServerError()

    def update(self, request, pk=None):
        """Handle PUT requests for an event
        Returns:
            Response -- Empty body with 204 status code
        """
        comment = Comment.objects.get(pk=pk)
        comment.content = request.data["content"]
        # comment.created_on = request.data["created_on"]

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single comment

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to comments resource

        Returns:
            Response -- JSON serialized list of comments
        """
        comments = Comment.objects.all()

        # Support filtering comments by label
        author = self.request.query_params.get('author', None)
        if author is not None:
            comments = comments.filter(author=author)

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for event host's related Django user"""
    class Meta:
        model = RareUser
        fields = ('first_name', 'last_name', 'email', 'username')


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    author = UserSerializer(many=False)
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on')
        depth = 1
