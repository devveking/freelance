
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        error_messages={'required': 'Пожалуйста, введите email'}
    )
    phone_number = forms.CharField(
        required=True,
        error_messages={'required': 'Пожалуйста, введите номер телефона'}
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')
        error_messages = {
            'username': {
                'required': 'Пожалуйста, введите имя пользователя',
                'unique': 'Это имя уже занято',
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _('Пароли не совпадают'))



from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите email',
            'class': 'input-field'
        }),
        error_messages={'required': 'Пожалуйста, введите email'}
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
        error_messages={'required': 'Пожалуйста, введите пароль'}
    )
