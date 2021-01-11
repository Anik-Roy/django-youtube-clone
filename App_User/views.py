from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CreateNewUser, UserLoginForm, EditProfileForm
from .models import UserProfile, Follow

from App_Upload.forms import VideoPostForm
from App_Upload.models import VideoPost, Like, Unlike

from App_Upload import utils

# Create your views here.


def signup(request):
    form = CreateNewUser
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse('App_User:login'))
    return render(request, 'App_User/signup.html', context={'form': form})


def login_page(request):
    form = UserLoginForm
    message = None
    if request.session.get('message', False):
        message = request.session.get('message')
        request.session['message'] = None
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Upload:home'))

    return render(request, 'App_User/login.html', context={'form': form, 'message': message})


@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_User:login'))


@login_required
def profile(request):
    form = VideoPostForm
    following = Follow.objects.filter(follower=request.user)
    following_users_list = User.objects.filter(pk__in=following.values_list('following', flat=True))
    if request.method == 'POST':
        form = VideoPostForm(request.POST, request.FILES)
        if form.is_valid():
            video_obj = form.save(commit=False)
            video_obj.user = request.user
            video_obj.save()
            form.save_m2m()
            current_uploaded_video = VideoPost.objects.get(pk=video_obj.pk)

            if not current_uploaded_video.thumbnail:
                make_thumbnail = utils.generate_thumbnail(str(current_uploaded_video.video))
                current_uploaded_video.thumbnail = make_thumbnail
                current_uploaded_video.save()
                print(current_uploaded_video)

            return HttpResponseRedirect(reverse('App_User:profile'))
    return render(request, 'App_User/profile.html', context={'form': form,
                                                             'following_users_list': following_users_list})


@login_required
def edit_profile(request):
    current_user_profile = UserProfile.objects.get(user=request.user)
    following = Follow.objects.filter(follower=request.user)
    following_users_list = User.objects.filter(pk__in=following.values_list('following', flat=True))
    form = EditProfileForm(instance=current_user_profile)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=current_user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_User:profile'))
    return render(request, 'App_User/edit_profile.html', context={'form': form,
                                                                  'following_users_list': following_users_list})


def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    already_followed = None
    following_users_list = None
    if request.user.is_authenticated:
        following = Follow.objects.filter(follower=request.user)
        following_users_list = User.objects.filter(pk__in=following.values_list('following', flat=True))
        already_followed = Follow.objects.filter(follower=request.user, following=user)
    return render(request, 'App_User/user_profile.html', context={'user': user, 'already_followed': already_followed,
                                                                  'following_users_list': following_users_list})


@login_required
def follow(request, pk):
    following_user = User.objects.get(pk=pk)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('App_User:user-profile', kwargs={'pk': pk}))


@login_required
def unfollow(request, pk):
    following_user = User.objects.get(pk=pk)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('App_User:user-profile', kwargs={'pk': pk}))
