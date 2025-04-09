from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'budget', 'deadline', 'category', 'tags']
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'budget': 'Бюджет',
            'deadline': 'Срок выполнения',
            'category': 'Категория',
            'tags': 'Теги',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок задания'}),
            'description': forms.Textarea(attrs={'placeholder': 'Опишите задание', 'rows': 7}),
            'budget': forms.NumberInput(attrs={'placeholder': 'Напишите бюджет в ₸'}),
            'category': forms.TextInput(attrs={'placeholder': 'Введите категорий через запятую'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Введите теги через запятую'}),
        }
