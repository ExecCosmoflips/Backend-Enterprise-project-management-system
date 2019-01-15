from rest_framework import serializers
from .models import *


class ProjectSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'department', 'leader', 'full_name', 'title', 'content', 'begin_time', 'end_time')

    def get_full_name(self, obj):
        return obj.leader.profile.name

    def get_department(self, obj):
        return DepartmentSerializer(obj.department).data


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')

    def get_full_name(self, obj):
        return obj.leader.last_name + obj.leader.first_name


class UserInfoSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('user', 'name', 'department_id', 'access', 'department_name', 'license', 'email', 'phone')

    def get_department_name(self, obj):
        return obj.department.name


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        return UserInfoSerializer(obj.profile).data

    class Meta:
        model = User
        fields = ('id', 'profile')


class ProjectInfoSerializer(serializers.ModelSerializer):
    staff = serializers.SerializerMethodField()
    leader = serializers.SerializerMethodField()

    def get_staff(self, obj):
        return UserSerializer(obj.staff.all(), many=True).data

    class Meta:
        model = Project
        fields = ('id', 'title', 'leader', 'content', 'begin_time', 'end_time', 'staff')

    def get_leader(self, obj):
        return UserSerializer(obj.leader).data


class UserRequestSerializer(serializers.ModelSerializer):
    staff = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    class Meta:
        model = StaffRequest
        fields = ('id', 'project', 'department', 'whether', 'content', 'staff')

    def get_staff(self, obj):
        return UserSerializer(obj.staff).data

    def get_project(self, obj):
        return ProjectSerializer(obj.project).data


class ProjectStaffSrializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'staff')
    def get_staff(self, obj):
        return UserInfoSerializer(obj.staff).data

