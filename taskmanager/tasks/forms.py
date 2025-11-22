from django import forms
from tasks.models import Task, Profile
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['owner', 'created_at', 'updated_at']
        
        widget = {
            'due_date': forms.DateInput(attrs={
                'type' : 'date',
                'class' : 'form-control'
            }),
            
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'avatar', 'birth_date', 'location', 'website']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }