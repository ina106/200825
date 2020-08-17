from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta: #Meta클래스는 한줄 띄고 적는게 좋아용
        model = Comment
        fields=('content',)