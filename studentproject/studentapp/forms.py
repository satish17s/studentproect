from django.forms import ModelForm
from .models import Student
from django import forms

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['name','subject','marks']


        widgets = {
            'name': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),

            'subject': forms.TextInput(
    				attrs={
    					'class': 'form-control'
    					}
    				),
            'marks': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),
                }
