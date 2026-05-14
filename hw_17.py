"""Задание 1:

Подумать, какой из видов пагинации более безопасный, чтобы не “светить” явно параметры в запросе. Выбрав нужный класс пагинации подключить глобальную пагинацию в проект. На одной странице должно располагаться не более 6 объектов.
"""


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "your_app.pagination.TaskCursorPagination",
}

from rest_framework.pagination import CursorPagination

class TaskCursorPagination(CursorPagination):
    page_size = 6
    ordering = "-created_at"
# по идее самая надежная, так как имеет закодированное состояние, а также меньше нагружает бд

"""
Задание 2:

Подключить систему логирования работы включенного сервера в проект для отслеживания логов работы приложения.
Логи должны загружаться следующим образом:
Отдельно логи работы включенного сервера с выводом в консоль
Отдельно логи HTTP запросов и их статусов в отдельную папку logs в корне проекта  в файл http_logs.log
Отдельно логи запросов в базу данных в отдельную папку logs в корне проекта в файл db_logs.log"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{levelname}] -> in {asctime} | {name} -> {message} |',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'http_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'http_logs.log'),
            'formatter': 'verbose',
        },
        'db_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'db_logs.log'),
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['http_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['db_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}