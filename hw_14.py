"""Задание 1:

Написать, или обновить, если уже есть, эндпоинт на получение списка всех задач по дню недели.
Если никакой параметр запроса не передавался - по умолчанию выводить все записи.
Если был передан день недели (например вторник) - выводить список задач только на этот день недели.
"""
from rest_framework import serializers, status
from my_app.models import Task, SubTask
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from hw_13 import SubTaskSerializer
from rest_framework.views import APIView


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'due_date', 'created_at', 'subtasks']

WEEKDAY_MAP = {
    "sunday": 1,
    "monday": 2,
    "tuesday": 3,
    "wednesday": 4,
    "thursday": 5,
    "friday": 6,
    "saturday": 7,
}

class TaskListView1(APIView):
    def get(self, request):
        weekday = request.query_params.get('weekday')
        tasks = Task.objects.all()
        if weekday:
            weekday_number = WEEKDAY_MAP.get(weekday.lower())
            if weekday_number is None:
                return Response({"error": "Not correct weekday"}, status=status.HTTP_400_BAD_REQUEST)
            tasks = tasks.filter(due_date__week_day=weekday_number)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)



"""
Задание 2:
Добавить пагинацию в отображение списка подзадач. На одну страницу должно отображаться не более 5 объектов. Отображение объектов должно идти в порядке убывания даты (от самого последнего добавленного объекта к самому первому)
"""


class SubTaskPagination(PageNumberPagination):
    page_size = 5

class SubTaskListView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all().order_by('-created_at')
        paginator = SubTaskPagination()
        paginated_subtasks = paginator.paginate_queryset(subtasks, request)
        serializer = SubTaskSerializer(paginated_subtasks, many=True)
        return paginator.get_paginated_response(serializer.data)

"""
Задание 3:
Добавить или обновить, если уже есть, эндпоинт на получение списка всех подзадач по названию главной задачи и статусу подзадач.
Если фильтр параметры в запросе не передавались - выводить данные по умолчанию, с учётом пагинации.
Если бы передан фильтр параметр названия главной задачи - выводить данные по этой главной задаче.
Если был передан фильтр параметр конкретного статуса подзадачи - выводить данные по этому статусу.
"""

class SubTaskFilterListView(APIView):
    def get(self, request):
        task_title = request.query_params.get('task')
        status_param = request.query_params.get('status')
        subtasks = SubTask.objects.all().order_by('-created_at')

        if task_title:
            subtasks = subtasks.filter(task__name__icontains=task_title)
        if status_param:
            subtasks = subtasks.filter(status__iexact=status_param)

        paginator = SubTaskPagination()
        paginated_subtasks = paginator.paginate_queryset(subtasks, request)
        serializer = SubTaskSerializer(paginated_subtasks, many=True)
        return paginator.get_paginated_response(serializer.data)