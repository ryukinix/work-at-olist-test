import uuid
from django.db import models


class SetModel(models.Model):
    """
    Base class as a mathematical set.
    Has a identifier UUID as its primary key and a field name unique.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        abstract = True  # define a abstract base class

    def __str__(self):
        return self.name


class Channel(SetModel):
    """
    Set of Channels. As defined on the SetModel: has a unique identifier
    and the field name as unique.
    """
    pass


class Category(SetModel):
    """
    Set of Categories. Must have a unique identifier, the category name,
    the channel name whose the category belongs and a possible parent.
    """
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    parent = models.ForeignKey('Category', null=True, blank=True,
                               related_name='children')

    @property
    def parents(self):
        """Return a list of the parents in order"""
        if self.parent:
            return self.parent.parents + [self.parent]

        return []
