from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login, name='login'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.list_uploaded_files, name='list_uploaded_files'),
    path('download-file/<int:file_id>/', views.download_file, name='download_file'),
]
