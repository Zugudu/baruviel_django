from django import forms
from .models import Task


# class _TaskNew(forms.Form):
# 	name = forms.CharField(max_length=20, label='Назва')
#
#
class TaskNew(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['name']