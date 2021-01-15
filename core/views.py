from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from bar import settings

from . import models


@login_required()
def index(request):
	context = []
	for i in models.Task.objects.all():
		status = True
		for j in i.subtask_set.all():
			if not j.done:
				status = False
		context.append({'status': status, 'task': i})
	return render(request, 'core/task_list.html', {'context': context})


class TaskDetail(LoginRequiredMixin, DetailView):
	model = models.Task
	context_object_name = 'task'


def task_delete(request, pk):
	task = get_object_or_404(models.Task, pk=pk)
	if request.user.id == task.who.id:
		task.delete()
	# else:
	# 	log_this_shit
	# TODO: make logging
	return HttpResponseRedirect(request.GET.get('next', reverse('index')))


def login_page(request):
	if request.method == 'POST':
		try:
			user = authenticate(request, username=request.POST['login'], password=request.POST['pass'])
			if user is None:
				return render(request, 'core/login.html', {'error': 'Невірні вхідні дані'})
			else:
				login(request, user)
				return HttpResponseRedirect(request.POST.get('next', settings.LOGIN_REDIRECT_URL))
		except KeyError:
			pass
	return render(request, 'core/login.html', {'next': request.GET.get('next', settings.LOGIN_REDIRECT_URL)})


def logout_page(request):
	logout(request)
	return HttpResponseRedirect(settings.LOGIN_URL)