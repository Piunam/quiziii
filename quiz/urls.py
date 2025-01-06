from .views import QuizListView, QuizDetailView
# from django.contrib import admin
from django.urls import path, include
from . import views


<<<<<<< HEAD
app_name = 'quiz'

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('admin/dashboard/', views.custom_admin_dashboard, name='admin_dashboard'),
=======

app_name = 'quiz'

urlpatterns = [
    path('admin/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('admin/dashboard/', views.custom_admin_dashboard, name='admin_dashboard'),

    
    path('', QuizListView.as_view(), name='quiz_list'),
>>>>>>> 7e79dcb39adf4aace1ca4763daa5ae0b61a6bac4
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
]