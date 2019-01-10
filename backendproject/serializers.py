from rest_framework import serializers
from .models import *


class ProjectSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('department', 'leader', 'full_name', 'title', 'content', 'content', 'begin_time', 'end_time')

    def get_full_name(self, obj):
        return obj.leader.profile.name


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id')

    def get_full_name(self, obj):
        return obj.leader.last_name + obj.leader.first_name


class UserInfoSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('name', 'department', 'access')

    def get_department(self, obj):
        return obj.department.id


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        return UserInfoSerializer(obj.profile).data

    class Meta:
        model = User
        fields = ('id', 'profile')


class ProjectInfoSerializer(serializers.ModelSerializer):
    personnel = serializers.SerializerMethodField()

    def get_personnel(self, obj):

        return UserSerializer(obj.personnels.all(), many=True).data

    class Meta:
        model = Project
        fields = ('id', 'title', 'leader', 'title', 'content', 'begin_time', 'end_time', 'personnel')

