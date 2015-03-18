from rest_framework.viewsets import ModelViewSet
from serializers import TagSerializer
from models import Tag


# def tag_list(request):
#     if request.method == 'GET':
#         tags = Tag.objects.all()
#         serializer = TagSerializer(tags, many=True)
#         return serializer.data


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
