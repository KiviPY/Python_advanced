"""=======================SERIALIZERS======================="""
from asyncio import Task
from datetime import timezone, datetime

from rest_framework import serializers, viewsets, status
from my_app.models import SubTask, Category
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'name', 'description', 'status']

class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SubTask
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

        def create(self, validated_data):
            category_name = validated_data.get('name')
            if Category.objects.filter(name__iexact=category_name).exists():
                raise serializers.ValidationError('Category already exists')
            return Category.objects.create(**validated_data)

        def update(self, instance, validated_data):
            category_name = validated_data.get('name', instance.name)
            description = validated_data.get('description', instance.description)
            if Category.objects.filter(name__iexact=category_name).exclude(id=instance.id).exists():
                raise serializers.ValidationError('Category already exists')

            instance.name = category_name
            instance.description = description
            instance.save()
            return instance

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'deu_date', 'created_at', 'subtasks']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'deleted_at']

        def validate_deadline(self, value):
            if value < datetime.now(timezone.utc):
                raise serializers.ValidationError('Deadline date cannot be in the past')
            return value
"""=======================Views======================="""

class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self):
        try:
            return SubTask.objects.get(pk=self.kwargs['pk'])
        except SubTask.DoesNotExist:
            raise NotFound("Subtask not found")


    def get(self, request, pk):
        subtask = self.get_object()
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk):
        subtask = self.get_object()
        serializer = SubTaskSerializer(subtask, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        subtask = self.get_object()
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

