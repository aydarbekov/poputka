from django import forms
from webapp.models import Review


class ReviewForm(forms.ModelForm):
    # grade = forms.IntegerField(min_value=1, max_value=5, label='Оценка')

    class Meta:
        model = Review
        fields = ['text']

