from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Group
from .models import Post


def index(request):
    posts = Post.objects.all()[:10]
    context = {
        'posts': posts,
    }
    return render(
        request,
        'posts/index.html',
        context
    )


def group_list(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(
        request, 'posts/group_list.html', context
    )


def post_create(request):
    return HttpResponse('hello world')


def profile(request, username: str):
    user = get_object_or_404(User, username=username)
    return HttpResponse('hello world')


def post_detail(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return HttpResponse('h')


def post_edit(response, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return HttpResponse('h')
