from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Document
from .permissions import IsOwner
from .serializers import DocumentSerializer, DocumentQuerySerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            return qs.filter(user=self.request.user)
        return qs

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(query_serializer=DocumentQuerySerializer())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        query_serializer = DocumentQuerySerializer(data=self.request.query_params)
        query_serializer.is_valid(raise_exception=True)
        is_signed = query_serializer.validated_data.get('is_signed')
        start_date = query_serializer.validated_data.get('start_date')
        end_date = query_serializer.validated_data.get('end_date')

        if is_signed is not None:
            queryset = queryset.filter(signature_date__isnull=not is_signed)

        if start_date and end_date:
            queryset = queryset.filter(creation_date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(creation_date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(creation_date__lte=end_date)

        return queryset


class LogoutView(generics.GenericAPIView):
    @staticmethod
    @swagger_auto_schema(auto_schema=None)
    def get(request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')
