from rest_framework.viewsets import ModelViewSet
from serializers import TagSerializer
from models import Tag

__author__ = 'assaf'

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
