from django.urls import path
from App_User import views

app_name = 'App_User'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('user-profile/<pk>/', views.user_profile, name='user-profile'),
    path('follow/<pk>/', views.follow, name='follow'),
    path('unfollow/<pk>/', views.unfollow, name='unfollow'),
]
