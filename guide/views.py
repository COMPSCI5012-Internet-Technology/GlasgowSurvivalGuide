from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from guide.forms import CommentForm, EmailLoginForm, PostForm, RegisterForm
from guide.models import Post,Category


def index(request):
    return render(request, 'guide/index.html')


@login_required
def about(request):
    return HttpResponse("Glasgow Survival Guide – about.")


def register(request):
    if request.user.is_authenticated:
        return redirect('guide:index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('guide:index')
    else:
        form = RegisterForm()
    return render(request, 'guide/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('guide:index')
    next_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = EmailLoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or ''
            if next_url:
                return redirect(next_url)
            return redirect('guide:index')
    else:
        form = EmailLoginForm()
    return render(request, 'guide/login.html', {'form': form, 'next': next_url})


def post_list(request):
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', 'newest').strip()
    if sort != 'oldest':
        sort = 'newest'

    if request.user.is_authenticated:
        post_list_qs = Post.objects.filter(
            Q(status=True) | Q(author=request.user)
        )
    else:
        post_list_qs = Post.objects.filter(status=True)
    if q:
        post_list_qs = post_list_qs.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        )
    if category_id and category_id.isdigit():
        id_val = int(category_id)
        if Category.objects.filter(pk=id_val).exists():
            post_list_qs = post_list_qs.filter(category_id=id_val)
        else:
            category_id = ''

    if sort == 'oldest':
        post_list_qs = post_list_qs.order_by('created_at')
    else:
        post_list_qs = post_list_qs.order_by('-created_at')

    categories = Category.objects.all().order_by('name')
    return render(
        request,
        'guide/post_list.html',
        {
            'post_list': post_list_qs,
            'q': q,
            'categories': categories,
            'category_id': category_id,
            'sort': sort,
        },
    )


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('guide:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'guide/post_form.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.status and (
        not request.user.is_authenticated or request.user != post.author
    ):
        raise Http404
    comment_list = post.comments.all().order_by('created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        if request.POST.get('comment_form'):
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('guide:post_detail', pk=post.pk)
        else:
            form = CommentForm()
    else:
        form = CommentForm()

    is_liked = False
    is_saved = False
    if request.user.is_authenticated:
        is_liked = post.liked_by.filter(pk=request.user.pk).exists()
        is_saved = post.saved_by.filter(pk=request.user.pk).exists()

    return render(
        request,
        'guide/post_detail.html',
        {
            'post': post,
            'comment_list': comment_list,
            'comment_form': form,
            'is_liked': is_liked,
            'is_saved': is_saved,
        },
    )


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.status and request.user != post.author:
        raise Http404
    if post.liked_by.filter(pk=request.user.pk).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    next_url = request.GET.get('next') or request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('guide:post_detail', pk=post.pk)


@login_required
def post_save(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.status and request.user != post.author:
        raise Http404
    if post.saved_by.filter(pk=request.user.pk).exists():
        post.saved_by.remove(request.user)
    else:
        post.saved_by.add(request.user)
    next_url = request.GET.get('next') or request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('guide:post_detail', pk=post.pk)
