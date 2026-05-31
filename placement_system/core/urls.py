
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='guest_home'),
    path('register/',views.register,name='register'),
    path('apply/<int:company_id>/',views.apply_company,name = 'apply_company'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('manage_applications/',views.company_dashboard,name ='manage_applications'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('student_home/',views.student_home,name = 'student_home'),
    path('company/<int:company_id>/', views.company_detail, name='company_detail'),
    path('update_application/<int:app_id>/', views.update_application, name='update_application'),
    path('manage_company/',views.manage_companies,name='manage_company'),
    path('delete_comapny/<int:company_id>/',views.delete_company,name='delete_company'),
    path('manage_students/',views.manage_students,name='manage_students'),
    path('profile/', views.student_profile, name='student_profile'),
    path('mock/', views.mock_list, name='mock_list'),
    path('mock/<int:test_id>/', views.take_mock, name='take_mock'),
    path('mock/submit/<int:test_id>/', views.submit_mock, name='submit_mock'),
    path('logout/', views.custom_logout, name='logout'),
]