from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('home/', views.home_page, name='home'),  # Added missing slash for better convention
    path('index/', views.index, name='index'),
    path('save_code/', views.save_code, name='save_code'),
    path('compile/', views.compile_code, name='compile'),
    path('view_pdf/<str:code>/<str:output>/', views.view_pdf, name='view_pdf'),
    path('view_pdf/', views.view_pdf, name='view_pdf_default'),
    path('generate_pdf/<str:code>/<str:output>/', views.generate_pdf, name='generate_pdf'),
    path('malpractice/', views.malpractice, name='malpractice'),
    path('mark-complete/', views.mark_complete, name='mark_complete'),  # New route for marking status
]
