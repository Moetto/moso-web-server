import json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from push_notifications.models import GCMDevice
from server.models import Group, GroupMember, Invite, Task, Location
from rest import InviteSerializer


@receiver(pre_save, sender=GroupMember)
def notify_group_update(sender, instance, **kwargs):
    try:
        old_member = GroupMember.objects.get(id=instance.id)
    except ObjectDoesNotExist:
        return
    old_group = old_member.group

    if old_group is not None and instance.group is not None:
        if old_group.id == instance.group.id:
            return

    if old_group is None and instance.group is None:
        return

    interested = []
    if old_group is not None:
        interested = list(GroupMember.objects.filter(group=old_group).values_list('id', flat=True))
    if instance.group is not None:
        interested.extend(GroupMember.objects.filter(group=instance.group).values_list('id', flat=True))
    print("Notigying group change")
    print(interested)
    GCMDevice.objects.filter(user__groupmember__id__in=interested).send_message(json.dumps({"action": "group_changed"}))


@receiver(post_save, sender=Location)
def notify_new_location(sender, instance, **kwargs):
    interested = instance.group.members.values_list('id', flat=True)
    GCMDevice.objects.filter(user__groupmember__id__in=interested).send_message(json.dumps({"action": "locations_changed"}))


@receiver(pre_save, sender=GroupMember)
def remove_empty_group(sender, **kwargs):
    print("Trying to remove empty groups")
    # TODO work work
    # Group.objects.filter(members=None).delete()


@receiver(post_save, sender=Invite)
def send_invite(sender, **kwargs):
    invite = kwargs['instance']
    serialized_invite = InviteSerializer(invite).data
    serialized_invite["group_name"] = invite.inviter.group.name
    serialized_invite["inviter_name"] = invite.inviter.name
    serialized_invite["action"] = "invite"
    serialized_invite["group_id"] = invite.inviter.group.id
    GCMDevice.objects.filter(user=invite.invited.user).send_message(json.dumps(serialized_invite))


@receiver(post_save, sender=Task)
def task_change(sender, **kwargs):
    task = kwargs['instance']
    GCMDevice.objects.filter(user__id__in=task.creator.group.members.values_list('user__id', flat=True))\
        .send_message(json.dumps({'action': 'tasks_changed'}))

