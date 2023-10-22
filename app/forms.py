from django import forms
from .models import Post
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Post
        fields = ['title', 'content', 'topic']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'})
        }