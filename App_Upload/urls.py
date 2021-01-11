from django.urls import path
from App_Upload import views

app_name = 'App_Upload'

urlpatterns = [
    path('', views.home, name='home'),
    path('edit-uploaded-video/', views.edit_uploaded_video, name='edit-uploaded-video'),
    path('delete-uploaded-video/', views.delete_uploaded_video, name='delete-uploaded-video'),
    path('play_video/<pk>/', views.play_video, name='play-video'),
    path('user-like-video/', views.user_liked_video, name='user-like-video'),
    path('like-video/<pk>/', views.like, name='like-video'),
    path('unlike-video/<pk>/', views.unlike, name='unlike-video'),
    path('like-comment/<pk>/', views.like_comment, name='like-comment'),
    path('unlike-comment/<pk>/', views.unlike_comment, name='unlike-comment'),
]
