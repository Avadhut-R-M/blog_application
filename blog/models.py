from time import time
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField()
    updated = models.DateTimeField()

    def save(self, *args, **kwargs) -> None:
        _now = timezone.now()
        self.updated = _now
        if not self.id:
            self.created = _now
        return super(TimeStamped, self).save( *args, **kwargs)

class MultiLevelObjects(TimeStamped):
    class Meta:
        abstract = True

    root_node_type = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    root_node_id = models.IntegerField(null=True, blank=True, db_index=True)

class Blog(TimeStamped):
    text = models.TextField()
    title = models.CharField(max_length=100)
    writter = models.ForeignKey(User, related_name='user_blogs', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return '{} - {} {}'.format(self.title, self.writter.first_name, self.writter.last_name)

    def save(self, *args, **kwargs) -> None:
        self.writter = self.user
        return super(Blog, self).save( *args, **kwargs)


class Comment(MultiLevelObjects):
    text = models.TextField()
    writter = models.ForeignKey(User, related_name='user_comments', on_delete=models.PROTECT)

class Like(MultiLevelObjects):
    owner = models.ForeignKey(User, related_name='user_likes', on_delete=models.PROTECT)
