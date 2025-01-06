from .views import QuizListView, QuizDetailView
# from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('admin/dashboard/', views.custom_admin_dashboard, name='admin_dashboard'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
]