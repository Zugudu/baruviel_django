from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
	name = models.CharField(max_length=50, verbose_name='Назва цілі')
	who = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ким видане')

	class Meta:
		verbose_name='Ціль'
		verbose_name_plural='Цілі'
		permissions = [('are_staff', 'Є частиною Лісових Чортів'),]

	def __str__(self):
		return self.name


class Subtask(models.Model):
	name = models.TextField(verbose_name='Назва завдання')
	whom = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кому видане')
	done = models.BooleanField(verbose_name='Статус виконання')
	task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Належить до цілі')

	class Meta:
		verbose_name='Завдання'
		verbose_name_plural='Завдання'

	def __str__(self):
		return '[%s] %s' % (self.task.name, self.name)