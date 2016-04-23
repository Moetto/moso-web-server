from django.db.models import Q
from rest_framework import filters
from rest_framework import routers, serializers, viewsets

from server.models import Task, GroupMember, Group, Location, Invite
from rest_framework import permissions


class IsInTaskGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groupmember.group

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.groupmember and obj.creator.group == request.user.groupmember.group


class IsInTaskGroupFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(creator__group=request.user.groupmember.group)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'creator', 'responsible_member', 'id', 'description', 'deadline', 'estimated_completion_time', 'completed')
        read_only_fields = ('creator', 'id')

    def create(self, validated_data):
        request = self.context['request']
        validated_data['creator'] = request.user.groupmember
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # assert validated_data.get('responsible', None) and instance.responsible is not None
        return super().update(instance, validated_data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (IsInTaskGroupFilter,)
    permission_classes = (permissions.IsAuthenticated,)


class IsInSameGroupPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and obj.creator.group == request.user.groupmember.group


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ('user',)


class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer
    permission_classes = (IsInSameGroupPermission,)


class IsInGroupPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and obj == request.user.groupmember.group


class IsInGroupFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.groupmember.group:
            return queryset.filter(id=request.user.groupmember.group.id)
        else:
            return queryset.none()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'members')

    def create(self, validated_data):
        group = super().create(validated_data)
        group.members.add(self._context['request'].user.groupmember)
        self._context['request'].user.groupmember.save()
        return group


class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (IsInGroupFilter,)
    permission_classes = (IsInGroupPermission,)


class BelongsToSameGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.groupmember.group:
            return False
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if not request.user.groupmember.group:
            return False
        return obj.group == request.user.groupmember.group


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'longitude', 'latitude')

    def create(self, validated_data):
        validated_data['group'] = self.context['request'].user.groupmember.group
        return super().create(validated_data)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (BelongsToSameGroup,)


class InviteFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if not request.user.groupmember.group:
            return queryset.filter(invited=request.user.groupmember)
        return queryset.filter(Q(invited__id__in=request.user.groupmember.group.members.values_list('id', flat=True)) |
                               Q(inviter__id__in=request.user.groupmember.group.members.values_list('id', flat=True)) |
                               Q(invited=request.user.groupmember))


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ('id', 'inviter', 'invited')


class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
