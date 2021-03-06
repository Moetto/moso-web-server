from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from server.models import Task, Group, GroupMember, Location, Invite


class FamilyMemberInline(admin.StackedInline):
    model = GroupMember


class UserAdmin(UserAdmin):
    inlines = [FamilyMemberInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Task)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Location)
admin.site.register(Invite)
