# problems/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.problem_list, name='problem_list'),  # /problems/
    path('add/', views.add_problem_view, name='add_problem'),  # /problems/add/
    path('manage/', views.manage_problems_view, name='manage_problems'),  # /problems/manage/
    path('run/', views.run_code_view, name='run_code'),  # /problems/run/
    path('<str:code>/', views.problem_detail, name='problem_detail'),  # /problems/PB001/
    path('<str:code>/update/', views.update_problem_view, name='update_problem'),  # /problems/PB001/update/
    path('<str:code>/delete/', views.delete_problem_view, name='delete_problem'),  # /problems/PB001/delete/
]
