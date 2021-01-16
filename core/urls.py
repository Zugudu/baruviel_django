from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.LoginPage.as_view(), name='login'),
	path('logout', views.logout_page, name='logout'),
	path('task/<int:pk>', views.TaskDetail.as_view(), name='task'),
	path('task/remove/<int:pk>', views.task_delete, name='task_delete'),
	path('task/new', views.TaskNew.as_view(), name='task_new'),
]