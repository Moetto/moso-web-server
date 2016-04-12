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
    user = models.OneToOneField(User, blank=True, null=True)
    group = models.ForeignKey('Group', related_name='members', null=True, blank=True)
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
    longitute = models.FloatField()
    latiture = models.FloatField()
