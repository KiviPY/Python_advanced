"""Домашнее задание: Реализация аутентификации JWT и пермишенов. Глобальная пагинация.
Цель:
Настроить JWT (JSON Web Token) аутентификацию с использованием SimpleJWT и реализовать пермишены для защиты API. Убедитесь, что только авторизованные пользователи могут выполнять определённые действия.

Задание 1: Настройка JWT аутентификации
Шаги для выполнения:

Установите djangorestframework-simplejwt.
Убедитесь, что библиотека djangorestframework-simplejwt установлена.
Настройте аутентификацию в settings.py.
Добавьте конфигурации SimpleJWT в settings.py.
Добавьте маршруты для получения и обновления JWT токенов.
Настройте маршруты для получения и обновления JWT токенов.
Проверьте что эндпоинты работают.
Проверьте что маршруты для получения и обновления JWT токенов работают.
"""
from datetime import timedelta

import permission
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
]


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()), # получить токены
    path('api/token/refresh/', TokenRefreshView.as_view()), # обновить access токен
]

"""Задание 2:
Реализаця пермишенов для API
Шаги для выполнения:
Продумайте пермишены.
Продумайте какие пермишены должны быть на представлениях.
Примените пермишены к API представлениям.
Добавьте пермишены ко всем представлениям.
Проверьте что пермишены работают.
Проверьте что пермишены работают согласно их настройкам."""


class TaskListView(APIView):
    permission_classes = [permissions.IsAuthenticated]


class SubTaskListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUser]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


"""Задание 3: Настройка глобальной пагинации в проекте

Обновить настройки проекта:
Подключить в настройках проекта Django REST framework глобальную пагинацию, выбрав класс пагинации из тех, что рассматривались на занятиях.
Протестировать эндпоинты:
Установить для пагинации возврат 5-ти элементов по умолчанию.
Проверить работу эндпоинтов с добавлением пагинации"""

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}
