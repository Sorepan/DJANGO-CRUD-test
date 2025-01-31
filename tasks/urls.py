from django.urls import path
from .views import home, signup, tasks, signout, signin, create_task, task, edit_task, complete_task, completed_tasks, delete_task

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('pending-tasks/', tasks, name='tasks'),
    path('completed-tasks/', completed_tasks, name='completed_tasks'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/', task, name='task'),
    path('tasks/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('tasks/<int:task_id>/complete/', complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('logout/', signout, name='logout'),
    path('login/', signin, name='login'),
]
