from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response


from projects.models import Task
from projects.serializers import (
    TaskListSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskUpdateSerializer
)
from projects.serializers.tasks import TaskSerializer
from datetime import datetime
from django.db.models.aggregates import Count


@api_view(['GET'])
def get_all_tasks(request: Request) -> Response:
    queryset = Task.objects.all()
    serialized_data = TaskSerializer(queryset, many=True)

    return Response(
        data=serialized_data.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def create_task(request: Request) -> Response:
    try:
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_task_by_id(request: Request, pk: int) -> Response:
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist as e:
        return Response(data={'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskDetailSerializer(task)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_statistic(request: Request) -> Response:
    tasks_count = Task.objects.all().count()
    status_count = Task.objects.values('status').annotate(count=Count('id')) # <QuerySet [{"status": "done", "count": 3}]>
    overdue_count = Task.objects.filter(due_date__lt=datetime.now()).exclude(status__in=["3", "4"]).count()
    return Response(
        data={'total_tasks': tasks_count, 'tasks_by_status': {item['status']: item['count'] for item in status_count}, 'overdue_count': overdue_count},
        status=status.HTTP_200_OK
    )

