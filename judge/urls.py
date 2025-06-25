from django.urls import path
from . import views
from .views import home_view, run_code_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view, name='home'), # This is the home page

    path('problems/', views.problem_list, name='problem_list'),
    path('problems/<str:code>/', views.problem_detail, name='problem_detail'),
    path('submissions/<int:id>/', views.submission_detail, name='submission_detail'),
    path('run-code/', run_code_view, name='run_code'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]