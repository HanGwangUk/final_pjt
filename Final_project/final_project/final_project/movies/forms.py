from django import forms
from .models import *


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['rank']