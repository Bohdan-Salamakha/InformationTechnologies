from django.urls import path

from .views import RaiseExceptionView

urlpatterns = [
    path('exceptions/', RaiseExceptionView.as_view(), name='exceptions'),
]

app_name = 'lab4'
