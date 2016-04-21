from server.models import GroupMember


def send_messge(group_member, message):
    print("Sent message")

def send_all(message):
    for member in GroupMember.objects.all():
        send_messge(member, message)