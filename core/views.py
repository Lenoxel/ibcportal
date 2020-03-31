from django.shortcuts import render, get_object_or_404
from .models import Post, Video, Schedule
from django.utils import timezone
from django.db.models import Q
from .models import PostView

def home(request):
    posts = Post.objects.filter(Q(published_date__lte=timezone.now()) | Q(published_date__isnull=True)).order_by('-published_date')
    meetings = Schedule.objects.filter(
        Q(start_date__gte=timezone.now()) | 
        Q(
            Q(end_date__isnull=False),
            end_date__lt=timezone.now()
        )
    )
    context = {
        'posts': posts,
        'meetings': meetings
    }
    return render(request, 'core/home.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post is not None:
        post_view, create = PostView.objects.get_or_create(post=post)
        if post_view:
            post_view.views_count += 1
            post_view.save()
    context = {
        'post': post
    }
    return render(request, 'core/post_detail.html', context)
    
