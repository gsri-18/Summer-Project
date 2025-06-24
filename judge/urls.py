from django.urls import path
from . import views
from .views import home_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view, name='home'), # This is the home page
    path('problems/', views.problem_list, name='problem_list'),
    path('problems/<str:code>/', views.problem_detail, name='problem_detail'),
    path('register/', views.register_view, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]