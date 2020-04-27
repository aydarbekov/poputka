from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput
from accounts.models import Profiles


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Почта')

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Имя пользователя'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise ValidationError('Email has already registered', code='email_registered')
        except User.DoesNotExist:
            return email


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Имя пользователя'
        }


class ProfileForm_2(forms.ModelForm):
    class Meta:
        model = Profiles
        exclude = ['user', 'ban']
        widgets = {
            'mobile_phone': TextInput(attrs={'placeholder': 'Моб. номер в формате +996555123456'}),
        }


class UserChangePasswordForm(forms.ModelForm):
    password = forms.CharField(max_length=100, required=True, label='New Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, required=True, label='New Password confirm', widget=forms.PasswordInput)
    old_password = forms.CharField(max_length=100, required=True, label='Old Password', widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.instance
        if not user.check_password(old_password):
            raise ValidationError('Invalid password.', code='invalid_password')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_confirm']
        if password_1 != password_2:
            raise ValidationError('Passwords do not match', code='passwords_do_not_match')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']


class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label='Поиск')
    in_first_name = forms.BooleanField(initial=False, required=False, label='По фамилии, имени')
    in_username = forms.BooleanField(initial=False, required=False, label='По Username')
    in_phone = forms.BooleanField(initial=False, required=False, label='По телефону')

    def clean(self):
        super().clean()
        data = self.cleaned_data
        text = data.get('text')
        # user = data.get('user')
        if not (text):
            raise ValidationError('Вы не ввели текст поиска!',
                                  code='text_search_empty')
        errors = []
        if text:
            in_username = data.get('in_username')
            in_first_name = data.get('in_first_name')
            in_phone = data.get('in_phone')
            if not (in_username or in_first_name or in_phone):
                errors.append(ValidationError(
                    'Пожулайста отметте критерии поиска, выставите галочки, где необходимо искать',
                    code='text_search_criteria_empty'
                ))
        if errors:
            raise ValidationError(errors)
        return data