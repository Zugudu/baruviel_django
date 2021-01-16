from django import forms
from .models import Task


class LoginPage(forms.Form):
	login = forms.CharField(widget=forms.TextInput(
		attrs={'class': 'w3-input', 'placeholder': 'Лоґін'}),
		label='Лоґін',
		label_suffix=''
	)
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'w3-input', 'placeholder': 'Пароль'}),
		label='Пароль',
		label_suffix=''
	)



class TaskNew(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['name']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'w3-input', 'placeholder': 'Назва цілі'})
		}