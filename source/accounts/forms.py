from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from accounts.models import Profiles


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise ValidationError('Email has already registered', code='email_registered')
        except User.DoesNotExist:
            return email


class ProfileForm_2(forms.ModelForm):
    class Meta:
        model = User
        exclude = []


ProfileFormset = inlineformset_factory(User, Profiles, ProfileForm_2, extra=1,
                                         can_delete=True)


# class DateForm(forms.Form):
#     date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
