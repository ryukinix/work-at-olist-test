import uuid
from django.db import models


class Channel(models.Model):
    """
    Each channel has a unique identifier
    and a field name.
    """

    identifier = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Each category has a unique identifier,
    the category name and a possible parent. A category belongs to a channel.
    """
    identifier = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    parent = models.ForeignKey('Category', null=True, related_name='children')

    def __str__(self):
        return self.name

    @property
    def parents(self):
        """Return a list of the parents in order"""
        if self.parent:
            return self.parent.parents + [self.parent]

        return []

    @property
    def subcategories(self):
        """Return all the subcategories of the category"""
        return self.children.all()
