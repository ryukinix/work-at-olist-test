from rest_framework import serializers
from . import models


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Channel
        fields = ('name', 'identifier')


class CategoryNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name', 'parent_name', 'identifier')


class CategoryDetailSerializer(serializers.ModelSerializer):
    parents = CategoryNamesSerializer(many=True)
    subcategories = CategoryNamesSerializer(many=True)

    class Meta:
        model = models.Category
        fields = ('name', 'identifier', 'parents', 'subcategories')
