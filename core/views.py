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
		form = forms.LoginPage()
		next = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
		return render(request, 'core/login.html', {'next': next, 'form': form})

	def post(self, request):
		form = forms.LoginPage(request.POST)
		next = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
		if form.is_valid():
			try:
				user = authenticate(request,
					username=form.cleaned_data.get('login'),
					password=form.cleaned_data.get('password')
				)
				if user is None:
					return render(request, 'core/login.html', {
						'error': 'Невірні вхідні дані',
						'form': form,
						'next': next
					})
				else:
					login(request, user)
					return HttpResponseRedirect(next)
			except KeyError:
				pass
		return render(request, 'core/login.html', {'next': next, 'form': form})


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
		return render(request, 'core/task_new.html', {'form': form})

	def post(self, request):
		form = forms.TaskNew(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.who = request.user
			task.save()
			return HttpResponseRedirect(reverse('task', args=[task.id]))
		else:
			return render(request, 'core/task_new.html', {'form': form, 'error': 'Дані форми введено не вірно'})


class TaskEdit(LoginRequiredMixin, View):
	def get(self, request, pk):
		task = get_object_or_404(models.Task, pk=pk)
		if request.user.id == task.who.id:
			form = forms.TaskNew(instance=task)
			return render(request, 'core/task_edit.html', {'form': form})
		else:
			# TODO log this shit
			return HttpResponseRedirect(reverse('index'))
