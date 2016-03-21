from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey('GroupMember', related_name='creator')
    group = models.ForeignKey('Group')
    responsible_member = models.ForeignKey('GroupMember', related_name='responsible', null=True, blank=True)

    def __str__(self):
        return self.title


class GroupMember(models.Model):
    user = models.OneToOneField(User)
    group = models.ForeignKey('Group', related_name='members')

    def __str__(self):
        return self.user.username


class Group(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
