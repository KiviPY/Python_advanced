from datetime import datetime, timezone

from django.db.models import Count

from rest_framework import serializers, status
from rest_framework.decorators import action

from my_app.models import Task, SubTask, Category
from django.urls import path
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from hw_13 import CategoryCreateSerializer
from django.db import models


"""Домашнее задание: Реализация CRUD для категорий с использованием ModelViewSet, мягкое удаление.
Реализовать полный CRUD для модели категорий (Categories) с помощью ModelViewSet, добавить кастомный метод для подсчета количества задач в каждой категории. Реализовать систему мягкого удаления для категорий.


Задание 1: Реализация CRUD для категорий с использованием ModelViewSet
Шаги для выполнения:

Создайте CategoryViewSet, используя ModelViewSet для CRUD операций.
Добавьте маршрут для CategoryViewSet.
Добавьте кастомный метод count_tasks используя декоратор @action для подсчета количества задач, связанных с каждой категорией.
"""

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        tasks_count = category.tasks.count() # по related_name в Task.category
        return Response({
            'category': CategoryCreateSerializer(category).data,
            'tasks_count': tasks_count
        })

"or"

class CategoryCountSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'task_count', 'is_deleted']


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in {'list', 'count_tasks'}:
            return CategoryCountSerializer
        return CategoryCreateSerializer

    # Вариант Б — все категории с количеством задач
    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        queryset = self.get_queryset().annotate(task_count=Count('tasks'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
urlpatterns = router.urls

"""Задание 2: Реализация мягкого удаления категорий
Шаги для выполнения:

Добавьте два новых поля в вашу модель Category, если таких ещё не было.
В модели Category добавьте поля is_deleted(Boolean, default False) и deleted_at(DateTime, null=true)
Переопределите метод удаления, чтобы он обновлял новые поля к соответствующим значениям: is_deleted=True и дата и время на момент “удаления” записи
Переопределите менеджера модели Category
В менеджере модели переопределите метод get_queryset(), чтобы он по умолчанию выдавал только те записи, которые не “удалены” из базы.
"""
from django.utils import timezone

class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def get_all_deleted(self):
        return super().get_queryset().filter(is_deleted=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CategoryManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name