from django.urls import path
from . import views
from .views import home_view, promote_users_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view, name='home'), # This is the home page

    # path('problems/', views.problem_list, name='problem_list'), # Now handled in problems.urls
    # path('problems/<str:code>/', views.problem_detail, name='problem_detail'), # Now handled in problems.urls
    path('submissions/<int:id>/', views.submission_detail, name='submission_detail'),
    # path('run-code/', run_code_view, name='run_code'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),


    path('promote-users/', promote_users_view, name='promote-users'),
    # path('add-problem/', add_problem_view, name='add_problem'), # Now handled in problems.urls
    # path('update-problem/<str:code>/', update_problem_view, name='update_problem'), # Now handled in problems.urls
    # path('manage-problems/', views.manage_problems_view, name='manage_problems'), # Now handled in problems.urls
    # path('delete-problem/<str:code>/', views.delete_problem_view, name='delete_problem'), # Now handled in problems.urls

    path('compiler/', views.online_compiler, name='online_compiler'),
    path('ai/', views.ai_suggestions, name='ai_suggestions'),

    path('contests/', views.contest_list_view, name='contest_list'),
    path('contests/add/', views.add_contest_view, name='add_contest'),
    path('contests/<slug:code>/', views.contest_detail_view, name='contest_detail'),
    path('contests/<slug:code>/<str:problem_code>/', views.contest_problem_view, name='contest_problem'),
    

]