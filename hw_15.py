from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from my_app.models import Task, SubTask
from django.urls import path

from hw_13 import SubTaskSerializer
from hw_14 import TaskSerializer

"""Задание 1: Замена представлений для задач (Tasks) на Generic Views
Шаги для выполнения:

Замените классы представлений для задач на Generic Views:
Используйте ListCreateAPIView для создания и получения списка задач.
Используйте RetrieveUpdateDestroyAPIView для получения, обновления и удаления задач.
Реализуйте фильтрацию, поиск и сортировку:
Реализуйте фильтрацию по полям status и deadline.
Реализуйте поиск по полям title и description.
Добавьте сортировку по полю created_at.
"""


"in settings: "

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ]
}


class BaseAPIView:
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "deadline"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]


class TaskListCreateAPIView(BaseAPIView, ListCreateAPIView):
    pass


class TaskRetrieveUpdateDestroyAPIView(BaseAPIView, RetrieveUpdateDestroyAPIView):
    pass

urlpatterns = [
    path("tasks/", TaskListCreateAPIView.as_view()),
    path("tasks/<int:pk>/", TaskRetrieveUpdateDestroyAPIView.as_view()),
]

"""Задание 2: Замена представлений для подзадач (SubTasks) на Generic Views
Шаги для выполнения:

Замените классы представлений для подзадач на Generic Views:
Используйте ListCreateAPIView для создания и получения списка подзадач.
Используйте RetrieveUpdateDestroyAPIView для получения, обновления и удаления подзадач.
Реализуйте фильтрацию, поиск и сортировку:
Реализуйте фильтрацию по полям status и deadline.
Реализуйте поиск по полям title и description.
Добавьте сортировку по полю created_at."""




class SubTaskListCreateAPIView(BaseAPIView, ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class SubTaskRetrieveUpdateDestroyAPIView(BaseAPIView, RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


urlpatterns += [
    path("subtasks/", SubTaskListCreateAPIView.as_view()),
    path("subtasks/<int:pk>/", SubTaskRetrieveUpdateDestroyAPIView.as_view())
]


"""
Оформление ответа:
Предоставьте решение: Прикрепите ссылку на гит.
Скриншоты тестирования: Приложите скриншоты из браузера или Postman, подтверждающие успешное создание, обновление, получение и удаление данных через API."""