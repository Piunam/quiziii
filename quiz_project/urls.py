"""
URL configuration for quiz_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from quiz.admin import custom_admin_site  # Ensure this import exists
=======


>>>>>>> 7e79dcb39adf4aace1ca4763daa5ae0b61a6bac4

app_name = 'quiz'

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('quiz-admin/', custom_admin_site.urls),
    path('', include('quiz.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path('grappelli/', include('grappelli.urls')),
    path('', include('quiz.urls')),
]
>>>>>>> 7e79dcb39adf4aace1ca4763daa5ae0b61a6bac4

