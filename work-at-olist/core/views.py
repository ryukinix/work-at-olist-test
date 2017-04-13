from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

from .models import Channel, Category
from . import serializers


class ChannelList(APIView):
    """
    Retrieve the list of channels name
    """
    def get(self, request, format=None):
        channels = Channel.objects.all()
        serializer = serializers.ChannelSerializer(channels, many=True)
        return Response(serializer.data)


class ChannelDetail(APIView):
    """
    Retrieve all categories from a given channel
    """
    def get(self, request, channel_name, format=None):
        channel = get_object_or_404(Channel, name=channel_name)
        categories = channel.category_set.all()
        serializer = serializers.CategoryNamesSerializer(categories, many=True)
        return Response(serializer.data)


class ChannelCategory(APIView):
    """
    Retrieve the parents and subcategories from each named category
    """
    def get(self, request, channel_name, category_name, format=None):
        channel = get_object_or_404(Channel, name=channel_name)
        categories = Category.objects.filter(name=category_name,
                                             channel=channel)
        if len(categories) < 1:
            raise Http404

        cat = self._concat(categories)
        serializer = serializers.CategoryDetailSerializer(cat)
        return Response(serializer.data)

    @staticmethod
    def _concat(categories):
        """
        Concatenate multiple categories of a given QuerySet
        into a dummy Class defined with colletions.namedtuple

        The parents and subcategories of all instances of a same category
        is concatenated and created a new instance as namedtuple UniqueCategory.
        """
        from collections import namedtuple
        UniqueCategory = namedtuple('UniqueCategory', ['name',
                                                       'parents',
                                                       'subcategories'])
        parents = sum((list(x.parents) for x in categories), [])
        subcategories = sum((list(x.subcategories) for x in categories), [])

        return UniqueCategory(name=categories[0].name,
                              parents=parents,
                              subcategories=subcategories)
