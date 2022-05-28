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
