import json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from push_notifications.models import GCMDevice
from server.models import *
from serverproject.urls import InviteSerializer


@receiver(post_save, sender=GCMDevice)
def notify_update(sender, **kwargs):
    print("Saved")
    GCMDevice.objects.all().send_message("hello")
    #print(kwargs)


@receiver(pre_save, sender=GroupMember)
def remove_empty_group(sender, **kwargs):
    print("Trying to remove empty groups")
    new = kwargs['instance']

    Group.objects.filter(members=None).delete()


@receiver(post_save, sender=Invite)
def send_invite(sender, **kwargs):
    invite = kwargs['instance']
    GCMDevice.objects.filter(user=invite.invited).send_message(json.dumps(InviteSerializer(invite).data))
