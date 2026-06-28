from django.urls import path
from . import views

urlpatterns = [
    path('', views.timer_page, name='timer_page'),
    path('api/save-session/', views.save_session, name='save_session'),
    path('api/tasks/', views.task_api, name='task_api'),
    path('api/stats/', views.stats_api, name='stats_api'),
]
