from rest_framework import serializers
from models import *


__author__ = 'assaf'

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag