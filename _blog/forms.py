from django import forms 
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'put you message here'}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', ]

class SearchForm(forms.Form):
    q = forms.CharField()