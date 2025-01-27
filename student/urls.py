from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('compile/', views.compile_code, name='compile'),
    path('view-pdf/<str:code>/<str:output>/', views.view_pdf, name='view_pdf'),
    path('generate-pdf/<str:code>/<str:output>/', views.generate_pdf, name='generate_pdf'),
    path('malpractice/', views.malpractice, name='malpractice'),  # New route for malpractice page
]
