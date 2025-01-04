from .views import QuizListView, QuizDetailView
# from django.contrib import admin
from django.urls import path, include

app_name = 'quiz'

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
]