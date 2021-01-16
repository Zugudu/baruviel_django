from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View

from bar import settings

from . import models
from . import forms


class LoginPage(View):
	def get(self, request):
		next = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
		return render(request, 'core/login.html', {'next': next})

	def post(self, request):
		next = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
		try:
			user = authenticate(request, username=request.POST['login'], password=request.POST['pass'])
			if user is None:
				return render(request, 'core/login.html', {'error': 'Невірні вхідні дані'})
			else:
				login(request, user)
				return HttpResponseRedirect(next)
		except KeyError:
			return render(request, 'core/login.html', {'next': next})


def logout_page(request):
	logout(request)
	return HttpResponseRedirect(settings.LOGIN_URL)


@login_required()
def index(request):
	context = []
	for i in models.Task.objects.all():
		status = True
		for j in i.subtask_set.all():
			if not j.done:
				status = False
				break
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


class TaskNew(LoginRequiredMixin, View):
	def get(self, request):
		form = forms.TaskNew()
		return render(request, 'core/new_task.html', {'form': form})

	def post(self, request):
		form = forms.TaskNew(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.who = request.user
			task.save()
			return HttpResponseRedirect(reverse('task', args=[task.id]))
		else:
			return render(request, 'core/new_task.html', {'form': form, 'error': 'Дані форми введено не вірно'})
