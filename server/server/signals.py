from django.db.models.signals import post_save
from django.dispatch import receiver
from push_notifications.models import GCMDevice


@receiver(post_save, sender=GCMDevice)
def notify_update(sender, **kwargs):
    print("Saved")
    GCMDevice.objects.all().send_message("hello")
    #print(kwargs)
