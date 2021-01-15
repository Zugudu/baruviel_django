from django import forms


class TaskNew(forms.Form):
	name = forms.CharField(max_length=20, label='Назва')
