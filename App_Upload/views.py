from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from App_Upload.models import VideoPost, Like, Unlike, Comment, CommentLike, CommentUnlike
from App_Upload.forms import VideoPostForm, CommentForm
from App_User.models import Follow

from App_Upload import utils

# Create your views here.


def home(request):
    all_video_post = VideoPost.objects.all()
    following = None
    following_users_list = None

    if request.user.is_authenticated:
        following = Follow.objects.filter(follower=request.user)
        following_users_list = User.objects.filter(pk__in=following.values_list('following', flat=True))
    message = None
    if request.method == 'GET':
        search = request.GET.get('search', '')
        all_video_post = VideoPost.objects.filter(title__icontains=search)
        if not all_video_post:
            message = 'No results found!'

    return render(request, 'App_Upload/home.html', context={'all_video_post': all_video_post, 'following_users_list': following_users_list, 'message': message})


@login_required
def user_liked_video(request):
    likes_obj = Like.objects.filter(user=request.user)
    all_video_post = VideoPost.objects.filter(pk__in=likes_obj.values_list('video_post', flat=True))
    following = Follow.objects.filter(follower=request.user)
    following_users_list = User.objects.filter(pk__in=following.values_list('following', flat=True))
    return render(request, 'App_Upload/user_liked_video.html',
                  context={'all_video_post': all_video_post, 'following_users_list': following_users_list})


@login_required
def edit_uploaded_video(request):
    if request.method == 'POST':
        pk = request.POST.get('postId')
        current_post = VideoPost.objects.get(pk=pk)
        form = VideoPostForm(request.POST, request.FILES, instance=current_post)
        if form.is_valid():
            video = form.cleaned_data['video']
            thumbnail = form.cleaned_data['thumbnail']
            if video:
                current_post.video = video
                current_post.save()
                make_thumbnail = utils.generate_thumbnail(str(current_post.video))
                current_post.thumbnail = make_thumbnail
                current_post.save()
            elif thumbnail:
                current_post.thumbnail = thumbnail
                current_post.save()
            return HttpResponse('success')
        else:
            return HttpResponse('error')
    return HttpResponse('error')


@login_required
def delete_uploaded_video(request):
    if request.method == 'POST':
        pk = request.POST.get('postID')
        current_post = VideoPost.objects.get(pk=pk)
        try:
            current_post.delete()
            return HttpResponse('success')
        except Exception as e:
            return HttpResponse(e)
    return HttpResponse('error')


def play_video(request, pk):
    current_video = VideoPost.objects.get(pk=pk)
    current_video_author = User.objects.get(pk=current_video.user.pk)
    liked_users = Like.objects.filter(video_post=current_video)
    liked_users_list = liked_users.values_list('user', flat=True)
    unliked_users = Unlike.objects.filter(video_post=current_video)
    unliked_users_list = unliked_users.values_list('user', flat=True)
    comments = Comment.objects.filter(video_post=current_video)
    comments_liked_by_user = None
    comments_liked_by_user_list = []
    comments_unliked_by_user = None
    comments_unliked_by_user_list = []
    already_followed = None
    following = None
    following_users_list = None

    if request.user.is_authenticated:
        comments_liked_by_user = CommentLike.objects.filter(user=request.user)
        comments_liked_by_user_list = comments_liked_by_user.values_list('comment', flat=True)
        comments_unliked_by_user = CommentUnlike.objects.filter(user=request.user)
        comments_unliked_by_user_list = comments_unliked_by_user.values_list('comment', flat=True)
        already_followed = Follow.objects.filter(follower=request.user, following=current_video_author)
        following = Follow.objects.filter(follower=request.user)
        following_users_list = User.objects.filter(pk__in=following.values_list('following', flat=True))

    comment_form = CommentForm
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment_obj = comment_form.save(commit=False)
                comment_obj.video_post = current_video
                comment_obj.user = request.user
                comment_obj.save()
                comment_form = CommentForm
        else:
            request.session['message'] = 'Please login to comment!'
            return HttpResponseRedirect(reverse('App_User:login'))
    return render(request, 'App_Upload/play_video.html', context={'current_video': current_video,
                                                                  'liked_users_list': liked_users_list,
                                                                  'unliked_users_list': unliked_users_list,
                                                                  'already_followed': already_followed,
                                                                  'following_users_list': following_users_list,
                                                                  'comments': comments,
                                                                  'comment_form': comment_form,
                                                                  'comments_liked_by_user_list': comments_liked_by_user_list,
                                                                  'comments_unliked_by_user_list': comments_unliked_by_user_list,})


@login_required
def like(request, pk):
    liked_video = VideoPost.objects.get(pk=pk)
    liker_user = request.user
    already_liked = Like.objects.filter(user=liker_user, video_post=liked_video)
    already_unliked = Unlike.objects.filter(user=liker_user, video_post=liked_video)
    if already_unliked:
        already_unliked.delete()
    if not already_liked:
        like_obj = Like(user=request.user, video_post=liked_video)
        like_obj.save()
    else:
        already_liked.delete()
    return HttpResponseRedirect(reverse('App_Upload:play-video', kwargs={'pk': pk}))


@login_required
def unlike(request, pk):
    unliked_video = VideoPost.objects.get(pk=pk)
    unliker_user = request.user
    already_liked = Like.objects.filter(user=unliker_user, video_post=unliked_video)
    if already_liked:
        already_liked.delete()

    already_unliked = Unlike.objects.filter(user=unliker_user, video_post=unliked_video)
    if not already_unliked:
        unlike_obj = Unlike(user=unliker_user, video_post=unliked_video)
        unlike_obj.save()
    else:
        already_unliked.delete()
    return HttpResponseRedirect(reverse('App_Upload:play-video', kwargs={'pk': pk}))


@login_required
def like_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    already_liked = CommentLike.objects.filter(user=request.user, comment=comment)
    already_unliked = CommentUnlike.objects.filter(user=request.user, comment=comment)
    if already_unliked:
        already_unliked.delete()
    if already_liked:
        already_liked.delete()
    else:
        comment_like = CommentLike(user=request.user, comment=comment)
        comment_like.save()
    return HttpResponseRedirect(reverse('App_Upload:play-video', kwargs={'pk': comment.video_post.pk}))


@login_required
def unlike_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    already_liked = CommentLike.objects.filter(user=request.user, comment=comment)
    already_unliked = CommentUnlike.objects.filter(user=request.user, comment=comment)
    if already_liked:
        already_liked.delete()
    if already_unliked:
        already_unliked.delete()
    else:
        comment_unlike = CommentUnlike(user=request.user, comment=comment)
        comment_unlike.save()
    return HttpResponseRedirect(reverse('App_Upload:play-video', kwargs={'pk': comment.video_post.pk}))