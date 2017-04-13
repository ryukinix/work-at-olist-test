from rest_framework import serializers
from . import models


class ChannelSerializer(serializers.ModelSerializer):
    """Serialize the information of a Channel model"""
    class Meta:
        model = models.Channel
        fields = ('name', 'identifier')


class CategorySerializer(serializers.ModelSerializer):
    """Serialize the information of a Category model"""
    class Meta:
        model = models.Category
        fields = ('name', 'identifier')


class CategoryRootSerializer(serializers.ModelSerializer):
    """Based on root Category, serialize the whole tree (subcategories)"""
    class Meta:
        model = models.Category
        fields = ('name', 'identifier', 'subcategories')

    def get_fields(self):
        """Wrap get_fields to support self-referential on tree"""
        fields = super().get_fields()
        fields['subcategories'] = CategoryRootSerializer(many=True)
        return fields


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Serialize the subcategories and parents of a given Category
    """
    parents = CategorySerializer(many=True)
    subcategories = CategoryRootSerializer(many=True)

    class Meta:
        model = models.Category
        fields = ('name', 'identifier', 'parents', 'subcategories')
