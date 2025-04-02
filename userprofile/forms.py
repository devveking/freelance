from django import forms
from django.forms import inlineformset_factory
from .models import UserProfile, WorkExperience, Education

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'profile_image', 'background_image', 'role', 'bio', 'gender', 'birth_date', 'location', 'hourly_rate', 'project_rate','skills','categories']
        labels = {
            'first_name': 'Имя',
            'profile_image': 'Фото профиля',
            'background_image': 'Фон профиля',
            'role': 'Роль',
            'bio': 'О себе',
            'gender': 'Пол',
            'birth_date': 'Дата рождения',
            'location': 'Местоположение',
            'hourly_rate': 'Почасовая ставка (₸)',
            'project_rate': 'Проектная ставка (₸)',
            'skills': 'Навыки',
            'categories': 'Услуги',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}),
            'role': forms.TextInput(attrs={'placeholder': 'Ваша сфера'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Расскажите о себе', 'rows': 4}),
            'location': forms.TextInput(attrs={'placeholder': 'Ваш город'}),
            'hourly_rate': forms.NumberInput(attrs={'placeholder': 'Введите ставку в ₸/час'}),
            'project_rate': forms.NumberInput(attrs={'placeholder': 'Введите ставку за проект'}),
            'skills': forms.TextInput(attrs={'placeholder': 'Введите навыки через запятую'}),
            'categories': forms.TextInput(attrs={'placeholder': 'Введите список услуг через запятую'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company', 'role', 'period', 'description']
        labels = {
            'company': 'Компания',
            'role': 'Должность',
            'period': 'Период работы',
            'description': 'Описание',
        }
        widgets = {
            'company': forms.TextInput(attrs={'placeholder': 'Название компании'}),
            'role': forms.TextInput(attrs={'placeholder': 'Ваша должность'}),
            'period': forms.TextInput(attrs={'placeholder': 'Например: 2020-2023'}),
            'description': forms.Textarea(attrs={'placeholder': 'Опишите вашу работу', 'rows': 3}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'specialization', 'period']
        labels = {
            'institution': 'Учебное заведение',
            'specialization': 'Специализация',
            'period': 'Годы обучения',
        }
        widgets = {
            'institution': forms.TextInput(attrs={'placeholder': 'Название университета или школы'}),
            'specialization': forms.TextInput(attrs={'placeholder': 'Например: Программирование'}),
            'period': forms.TextInput(attrs={'placeholder': 'Например: 2015-2019'}),
        }

# Создаем formset'ы для редактирования множества объектов WorkExperience и Education
WorkExperienceFormSet = inlineformset_factory(UserProfile, WorkExperience, form=WorkExperienceForm, extra=1, can_delete=True)
EducationFormSet = inlineformset_factory(UserProfile, Education, form=EducationForm, extra=1, can_delete=True)

