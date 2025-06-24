from django.urls import path
from . import views
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'), # This is the home page
    path('problems/', views.problem_list, name='problem_list'),
    path('problems/<str:code>/', views.problem_detail, name='problem_detail'),
    path('register/', views.register_view, name='register'),
]