from django.urls import path
from . import api_views


urlpatterns = [
    path('task_create/', api_views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/', api_views.TaskListView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', api_views.TaskDetailView.as_view(), name='task'),
    path('api-token-auth/login/', api_views.LoginView.as_view(), name='login'),
    path('api-token-auth/register/', api_views.RegisterView.as_view(), name='register'),
]