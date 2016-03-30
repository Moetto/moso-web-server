"""serverproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import filters
from rest_framework import routers, serializers, viewsets

from server import views
from server.models import Task, GroupMember, Group
from rest_framework import permissions


class IsInTaskGroupPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and obj.group == request.user.groupmember.group


class IsInTaskGroupFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(group=request.user.groupmember.group)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'creator', 'group', 'responsible_member')
        read_only_fields = ('creator', 'group')

    def create(self, validated_data):
        request = self.context['request']
        validated_data['creator'] = request.user.groupmember
        validated_data['group'] = request.user.groupmember.group
        return super().create(validated_data)

    def update(self, instance, validated_data):
        assert validated_data.get('responsible', None) and instance.responsible is not None
        return super().update(instance, validated_data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (IsInTaskGroupFilter,)
    permission_classes = (permissions.IsAuthenticated,)


class IsInSameGroupPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and obj.group == request.user.groupmember.group


class IsInSameGroupFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(group=request.user.groupmember.group)


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ('user',)


class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer
    filter_backends = (IsInSameGroupFilter,)
    permission_classes = (IsInSameGroupPermission,)


class IsInGroupPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and obj == request.user.groupmember.group


class IsInGroupFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(id=request.user.groupmember.group.id)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'members')


class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (IsInGroupFilter,)
    permission_classes = (IsInGroupPermission,)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'groupmembers', GroupMemberViewSet)
router.register(r'groups', GroupsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^register/$', views.get_auth_token, name='register'),
    url(r'', include('gcm.urls')),
]

