from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
	name = models.CharField(max_length=20)
	who = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name='Ціль'
		verbose_name_plural='Цілі'

	def __str__(self):
		return self.name


class Subtask(models.Model):
	name = models.TextField()
	whom = models.ForeignKey(User, on_delete=models.CASCADE)
	done = models.BooleanField()
	task = models.ForeignKey(Task, on_delete=models.CASCADE)

	class Meta:
		verbose_name='Завдання'
		verbose_name_plural='Завдання'

	def __str__(self):
		return '[%s] %s' % (self.task.name, self.name)