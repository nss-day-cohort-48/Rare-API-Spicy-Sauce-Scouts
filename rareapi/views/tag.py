"""View module for handling requests about tags"""
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Tag


class TagView(ViewSet):
    """Rare tags"""

    def create(self, request):
        """Handle POST operations for tags

        Returns:
            Response -- JSON serialized tags 
        """
        tag = Tag.objects.get()
        tag = Tag()
        tag.label = request.data["label"]

        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag

        Returns:
            Response -- JSON serialized Tag
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponseServerError()

    def update(self, request, pk=None):
        """Handle PUT requests for an event
        Returns:
            Response -- Empty body with 204 status code
        """
        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]

        tag.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single tag

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to tags resource

        Returns:
            Response -- JSON serialized list of tags
        """
        tags = Tag.objects.all()

        # Support filtering tags by label
        label = self.request.query_params.get('label', None)
        if label is not None:
            tags = tags.filter(label=label)

        serializer = TagSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label')
