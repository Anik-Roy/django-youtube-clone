from django import forms
from .models import VideoPost, Comment


class VideoPostForm(forms.ModelForm):
    video = forms.FileField(widget=forms.FileInput(attrs={'accept': 'video/*'}))

    class Meta:
        model = VideoPost
        fields = ('title', 'video', 'thumbnail', )


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add a public comment...'}), label='')

    class Meta:
        model = Comment
        fields = ('comment', )

