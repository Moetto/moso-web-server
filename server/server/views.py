import json

from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from oauth2client import client, crypt
import uuid
# Create your views here.
from push_notifications.models import GCMDevice
from rest_framework.authtoken.models import Token

from server.models import GroupMember

CLIENT_ID = "727690215041-1oa6sfgn9u225i7m4gkrmkscmlojlqg5.apps.googleusercontent.com"
ANDROID_CLIENT_ID = "727690215041-1oa6sfgn9u225i7m4gkrmkscmlojlqg5.apps.googleusercontent.com"


class RegisterForm(forms.Form):
    token = forms.CharField()
    gcm_token = forms.CharField()


@csrf_exempt
def get_auth_token(request):
    if request.method == "POST":
        print(request.POST)
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Errors in form", status=400)

        try:
            idinfo = client.verify_id_token(form.cleaned_data['token'], CLIENT_ID)
            # If multiple clients access the backend server:
            if idinfo['aud'] not in [ANDROID_CLIENT_ID]:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
        except crypt.AppIdentityError as e:
            print(e)
            return HttpResponse("Invalid identity", status=400)
            # Invalid token
        userid = idinfo['sub']
        print("Userid: "+userid)
        member, created = GroupMember.objects.get_or_create(userid=str(userid))
        member.save()
        if created:
            user = User.objects.create(username=uuid.uuid4())
            member.user = user
            member.save()
            user.save()
            token = Token.objects.create(user=user)
            token.save()
            device = GCMDevice(registration_id=form.cleaned_data['gcm_token'], user=user)
            device.save()

        return HttpResponse(json.dumps({"token": str(Token.objects.get(user=member.user)),
                                       "group_member_id": member.id}))

    return HttpResponse("POST only", status=400)

