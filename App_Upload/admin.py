from django.contrib import admin
from .models import VideoPost, Like, Unlike, Comment, CommentLike, CommentUnlike

# Register your models here.
admin.site.register(VideoPost)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Unlike)
admin.site.register(CommentLike)
admin.site.register(CommentUnlike)
