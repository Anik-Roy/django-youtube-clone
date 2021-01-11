from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class VideoPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_video')
    title = models.CharField(max_length=264, blank=False)
    video = models.FileField(upload_to='upload_video', blank=False, null=False)
    thumbnail = models.ImageField(upload_to='upload_thumbnail', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title', ]


class Comment(models.Model):
    video_post = models.ForeignKey(VideoPost, on_delete=models.CASCADE, related_name='video_post_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-comment_date', )

    def __str__(self):
        return self.comment


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_liked_video')
    video_post = models.ForeignKey(VideoPost, on_delete=models.CASCADE, related_name='liked_video_post')
    like_date = models.DateTimeField(auto_now_add=True)


class Unlike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_unliked_video')
    video_post = models.ForeignKey(VideoPost, on_delete=models.CASCADE, related_name='unliked_video_post')
    unlike_date = models.DateTimeField(auto_now_add=True)


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_like')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    like_date = models.DateTimeField(auto_now_add=True)


class CommentUnlike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_unlike')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_unlikes')
    unlike_date = models.DateTimeField(auto_now_add=True)

