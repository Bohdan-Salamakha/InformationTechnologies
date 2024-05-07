import json

from django_redis import get_redis_connection
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from non_rel_db.models import Employee
from non_rel_db.serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    model_name = Employee.__name__.lower()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    connection = get_redis_connection()

    @swagger_auto_schema(auto_schema=None)
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        employee_pk = self.connection.incr('employee_id_counter')
        self.connection.set(
            f'{self.model_name}:{employee_pk}',
            json.dumps(serializer.validated_data)
        )
        serializer.validated_data['id'] = employee_pk

    def retrieve(self, request, *args, **kwargs):
        employee_pk = kwargs["pk"]
        employee_data = self.connection.get(f'{self.model_name}:{employee_pk}')
        if employee_data is None:
            raise NotFound(detail=f"{self.model_name} with pk {employee_pk} not found")
        serializer = self.get_serializer(data=json.loads(employee_data))
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = employee_pk
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        employee_pk = kwargs["pk"]
        employee_data = self.connection.get(f'{self.model_name}:{employee_pk}')
        if employee_data is None:
            raise NotFound(detail=f"{self.model_name} with pk {employee_pk} not found")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.connection.set(
            f'{self.model_name}:{employee_pk}',
            json.dumps(serializer.validated_data)
        )
        serializer.validated_data['id'] = employee_pk
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        employee_pk = kwargs["pk"]
        employee_data = self.connection.get(f'{self.model_name}:{employee_pk}')
        if employee_data is None:
            raise NotFound(detail=f"{self.model_name} with pk {employee_pk} not found")
        self.connection.delete(f'{self.model_name}:{employee_pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)
