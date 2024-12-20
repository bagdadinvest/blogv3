from django.urls import path
from .views import ShellEndpointView

urlpatterns = [
    path('shell/', ShellEndpointView.as_view(), name='shell-endpoint'),
]
