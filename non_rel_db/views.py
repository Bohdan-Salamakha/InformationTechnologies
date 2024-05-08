import json

from bson import ObjectId
from bson.errors import InvalidId
from django_redis import get_redis_connection
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from information_technologies.mongo_utils import students_collection
from non_rel_db.models import Employee, Student
from non_rel_db.serializers import EmployeeSerializer, StudentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    model_name = Employee.__name__.lower()
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
        employee_data = self.__check_employee_data(employee_pk)
        serializer = self.get_serializer(data=json.loads(employee_data))
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = employee_pk
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        employee_pk = kwargs["pk"]
        self.__check_employee_data(employee_pk)
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
        self.__check_employee_data(employee_pk)
        self.connection.delete(f'{self.model_name}:{employee_pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def __check_employee_data(self, employee_pk: str):
        employee_data = self.connection.get(f'{self.model_name}:{employee_pk}')
        if employee_data is None:
            raise NotFound(detail=f"{self.model_name} with pk {employee_pk} not found")
        return employee_data


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    model_name = Employee.__name__.lower()

    @swagger_auto_schema(auto_schema=None)
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        student = students_collection.insert_one(serializer.validated_data)
        serializer.validated_data['id'] = str(student.inserted_id)

    def retrieve(self, request, *args, **kwargs):
        student_pk = kwargs["pk"]
        student_data = self.__check_students_data(student_pk)
        serializer = self.get_serializer(data=student_data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = student_pk
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        student_pk = kwargs["pk"]
        self.__check_students_data(student_pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        students_collection.update_one(
            {'_id': ObjectId(student_pk)},
            {'$set': serializer.validated_data}
        )
        serializer.validated_data['id'] = student_pk
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        student_pk = kwargs["pk"]
        self.__check_students_data(student_pk)
        students_collection.delete_one({'_id': ObjectId(student_pk)})
        return Response(status=status.HTTP_204_NO_CONTENT)

    def __check_students_data(self, student_pk: str):
        try:
            student_data = students_collection.find_one({'_id': ObjectId(student_pk)})
        except InvalidId as e:
            raise ValidationError(detail=e)
        if student_data is None:
            raise NotFound(detail=f"{self.model_name} with pk {student_pk} not found")
        return student_data
