from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Review

class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class ReviewForm(forms.ModelForm):
    STAR_CHOICE = [
        ('1', '1'),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ]

    stars = forms.IntegerField(widget=forms.RadioSelect(choices=STAR_CHOICE))
    text = forms.CharField(label='Содержание:', widget = forms.Textarea(attrs={'class': 'form-control', 'plaсeholder': "Содержание комментария"}))

    class Meta:
        model = Review
        fields = ('stars', 'text')
        # widgets = {
        #     'text': forms.Textarea(attrs={'class': 'form-control', 'plaсeholder': "Содержание комментария"}),
        # }