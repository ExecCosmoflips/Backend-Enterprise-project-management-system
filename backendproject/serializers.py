from rest_framework import serializers
from .models import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('department', 'leader', 'title', 'content', 'content', 'begin_time', 'end_time')
