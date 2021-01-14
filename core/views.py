from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.views.generic import ListView, DetailView

from . import models


def index(request):
	context = []
	for i in models.Task.objects.all():
		status = True
		for j in i.subtask_set.all():
			if not j.done:
				status = False
		context.append({'status': status, 'task': i})
	return render(request, 'core/task_list.html', {'context': context})


class TaskDetail(DetailView):
	model = models.Task
	context_object_name = 'task'


def login_page(request):
	if request.method == 'POST':
		try:
			user = authenticate(request, username=request.POST['login'], password=request.POST['pass'])
			if user is None:
				return render(request, 'core/login.html', {'error': 'Невірні вхідні дані'})
			else:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
		except KeyError:
			pass
	return render(request, 'core/login.html')


def logout_page(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))