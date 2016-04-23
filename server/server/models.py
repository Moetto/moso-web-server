from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    creator = models.ForeignKey('GroupMember', related_name='creator')
    responsible_member = models.ForeignKey('GroupMember', related_name='responsible', null=True, blank=True)
    deadline = models.IntegerField(blank=True, null=True)
    estimated_completion_time = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class GroupMember(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    group = models.ForeignKey('Group', related_name='members', null=True, blank=True, on_delete=models.SET_NULL)
    userid = models.CharField(max_length=150)

    def __str__(self):
        try:
            return self.user.username
        except:
            return "Kikkeli"


class Group(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    longitude = models.FloatField()
    latitude = models.FloatField()
    group = models.ForeignKey(Group)


class Invite(models.Model):
    inviter = models.ForeignKey(GroupMember, related_name='sent_invite')
    invited = models.ForeignKey(GroupMember, related_name='received_invite')

from server.signals import *
