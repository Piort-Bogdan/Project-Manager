from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Project, Task, TimeTracker


class ProjectSerializer(serializers.ModelSerializer):
    team_members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        team_members = validated_data.pop('team_members')
        project = Project.objects.create(**validated_data)
        project.team_members.set(team_members)

        return project

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['team_members'] = [team_member.username for team_member in instance.team_members.all()]
        return data


class TaskSerializer(serializers.ModelSerializer):
    own_project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        assinged_to = validated_data.pop('assigned_to')
        task = Task.objects.create(**validated_data)
        task.assigned_to.set(assinged_to)
        return task

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['own_project'] = instance.own_project.title
        data['assigned_to'] = [team_member.username for team_member in instance.assigned_to.all()]
        return data


class TimeTrackerSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    team_member = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = TimeTracker
        fields = '__all__'

    def create(self, validated_data):
        time_tracker = TimeTracker.objects.create(**validated_data)
        return time_tracker

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        extra_kwargs.update({
            'task': {'help_text': 'The task for which time is being tracked'},
            'team_member': {'help_text': 'The team member tracking the time'},
        })
        return extra_kwargs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['task'] = instance.task.title
        data['team_member'] = instance.team_member.username
        return data


class ProjectErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
