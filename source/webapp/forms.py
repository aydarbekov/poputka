from django import forms
from webapp.models import Review, Announcements


class ReviewForm(forms.ModelForm):
    # grade = forms.IntegerField(min_value=1, max_value=5, label='Оценка')

    class Meta:
        model = Review
        fields = ['text']


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcements
        fields = ['type', 'description', 'place_from', 'place_to', 'departure_time', 'car', 'car_model', 'seats',
                  'luggage', 'price',
                  'photo']
