from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from .exceptions import *
from .serializers import ExceptionTypeSerializer, ExceptionResponseSerializer


class RaiseExceptionView(generics.GenericAPIView):
    serializer_class = ExceptionTypeSerializer

    @swagger_auto_schema(
        responses={500: ExceptionResponseSerializer(), 200: None}
    )
    def get(self, request, *args, **kwargs):
        raise UncheckedException("An unchecked exception occurred")

    @swagger_auto_schema(
        request_body=ExceptionTypeSerializer(),
        responses={400: ExceptionResponseSerializer(), 201: None}
    )
    def post(self, request, *args, **kwargs):
        serializer = ExceptionTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exc_type = serializer.validated_data['exception_type']

        if exc_type == 1:
            raise CustomException1("Error related to CustomException1")
        elif exc_type == 2:
            raise CustomException2("Error related to CustomException2")
        elif exc_type == 3:
            raise CustomException3("Error related to CustomException3")
        elif exc_type == 4:
            raise CustomException4("Error related to CustomException4")
        elif exc_type == 5:
            raise CustomException5("Error related to CustomException5")

        return Response({"message": "No exception thrown"})
