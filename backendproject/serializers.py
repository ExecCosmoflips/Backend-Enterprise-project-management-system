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