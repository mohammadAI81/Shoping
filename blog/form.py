from django import forms

from .models import Comment, Reply

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = "__all__"
