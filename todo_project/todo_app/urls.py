from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('add_todo', views.add_todo, name='add_todo'),
    path('completed/<int:task_id>', views.completed, name='completed'),
    path('completed_list', views.completed_list, name='completed_list'),
    path('delete/<int:task_id>', views.delete, name='delete'),
]

