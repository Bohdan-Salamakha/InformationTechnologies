from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, StudentViewSet

router = DefaultRouter()

router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'non_rel_db'
