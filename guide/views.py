from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from guide.forms import CommentForm, EmailLoginForm, PostForm, RegisterForm, UserProfileForm
from guide.models import Category, CollectionList, News, Post, UserProfile
from django.http import JsonResponse

from guide.forms import (
    CollectionCreateForm,
    CommentForm,
    EmailLoginForm,
    PostForm,
    RegisterForm,
    UserProfileForm,
)
from guide.utils import get_video_embed

User = get_user_model()


def index(request):
   return redirect('guide:post_list')


def news_list(request):
    news_items = News.objects.all().order_by("-time")
    return render(request, "guide/news_list.html", {"news_list": news_items})


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

def user_logout(request):
    logout(request)
    return redirect('guide:index')


@login_required
def profile_view(request):
    profile, _created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={"email": request.user.email or ""},
    )
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("guide:profile")
    else:
        form = UserProfileForm(instance=profile)

    user_posts = Post.objects.filter(author=request.user).select_related(
        "author__profile", "category"
    ).order_by("-created_at")
    saved_posts = request.user.saved_posts.all().select_related(
        "author__profile", "category"
    ).order_by("-created_at")

    active_tab = (request.GET.get("tab") or "posts").strip()
    if active_tab == "saved":
        tab_posts = saved_posts
    else:
        active_tab = "posts"
        tab_posts = user_posts

    return render(
        request,
        "guide/profile.html",
        {
            "profile": profile,
            "form": form,
            "user_posts": user_posts,
            "saved_posts": saved_posts,
            "active_tab": active_tab,
            "tab_posts": tab_posts,
        },
    )

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
    grouped_categories = {}
    for cat in categories:
        if " - " in cat.name:
            main_cat, sub_cat = cat.name.split(" - ", 1)
        else:
            main_cat = "General"
            sub_cat = cat.name
        if main_cat not in grouped_categories:
            grouped_categories[main_cat] = []
            
        grouped_categories[main_cat].append({
            'id': cat.id,
            'name': sub_cat  
        })
    recent_news = News.objects.all().order_by('-time')[:5]
    author_ids = list(set(post_list_qs.values_list('author_id', flat=True)))
    author_profiles = {
        p.user_id: p
        for p in UserProfile.objects.filter(user_id__in=author_ids)
    }
    post_list_with_profiles = [
        (post, author_profiles.get(post.author_id))
        for post in post_list_qs
    ]
    return render(
        request,
        'guide/post_list.html',
        {
            'post_list_with_profiles': post_list_with_profiles,
            'q': q,
            'categories': categories,
            'category_id': category_id,
            'sort': sort,
            'recent_news': recent_news,
            'grouped_categories': grouped_categories,
        },
    )


@login_required
def post_create(request):
    categories = Category.objects.all().order_by('name')
    grouped_categories = {}
    for cat in categories:
        if " - " in cat.name:
            main_cat, sub_cat = cat.name.split(" - ", 1)
        else:
            main_cat = "General"
            sub_cat = cat.name
            
        if main_cat not in grouped_categories:
            grouped_categories[main_cat] = []
            
        grouped_categories[main_cat].append({
            'id': cat.id,
            'name': sub_cat
        })
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('guide:post_list')
    else:
        form = PostForm()
    return render(
        request, 
        'guide/post_form.html', 
        {
            'form': form,
            'grouped_categories': grouped_categories 
        }
    )


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related("author__profile"), pk=pk
    )
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
    user_collections = []
    collection_ids_containing_post = set()
    if request.user.is_authenticated:
        is_liked = post.liked_by.filter(pk=request.user.pk).exists()
        is_saved = post.saved_by.filter(pk=request.user.pk).exists()
        user_collections = request.user.collections.all().order_by('name')
        collection_ids_containing_post = set(
            post.in_collections.filter(owner=request.user).values_list('pk', flat=True)
        )

    video_embed_url = None
    video_use_iframe = False
    if post.video and post.video.strip():
        video_embed_url, video_use_iframe = get_video_embed(post.video)

    return render(
        request,
        'guide/post_detail.html',
        {
            'post': post,
            'comment_list': comment_list,
            'comment_form': form,
            'is_liked': is_liked,
            'is_saved': is_saved,
            'user_collections': user_collections,
            'collection_ids_containing_post': collection_ids_containing_post,
            'video_embed_url': video_embed_url,
            'video_use_iframe': video_use_iframe,
        },
    )


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.status and request.user != post.author:
        raise Http404
        
    is_liked = False
    if post.liked_by.filter(pk=request.user.pk).exists():
        post.liked_by.remove(request.user)
        is_liked = False
    else:
        post.liked_by.add(request.user)
        is_liked = True
        
    return JsonResponse({'is_liked': is_liked, 'likes_count': post.liked_by.count()})


@login_required
def post_save(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.status and request.user != post.author:
        raise Http404
        
    is_saved = False
    if post.saved_by.filter(pk=request.user.pk).exists():
        post.saved_by.remove(request.user)
        is_saved = False
    else:
        post.saved_by.add(request.user)
        is_saved = True
        
    return JsonResponse({'is_saved': is_saved})


@login_required
def collection_list(request):
    collections = request.user.collections.all().order_by('name')
    return render(request, 'guide/collection_list.html', {'collections': collections})


@login_required
def collection_create(request):
    if request.method == 'POST':
        form = CollectionCreateForm(request.POST, user=request.user)
        if form.is_valid():
            CollectionList.objects.create(
                owner=request.user,
                name=form.cleaned_data['name'].strip(),
                status=form.cleaned_data['status'],
            )
            return redirect('guide:collection_list')
    else:
        form = CollectionCreateForm(user=request.user)
    return render(request, 'guide/collection_form.html', {'form': form})


@login_required
def collection_detail(request, pk):
    collection = get_object_or_404(CollectionList, pk=pk)
    if collection.owner != request.user:
        if not collection.status:
            raise Http404
    posts_in_collection = collection.posts.all().order_by('-created_at')
    return render(
        request,
        'guide/collection_detail.html',
        {'collection': collection, 'posts_in_collection': posts_in_collection},
    )


@login_required
def user_public_collections(request, user_id):
    target_user = get_object_or_404(
        User.objects.select_related("profile"), pk=user_id
    )
    public_collections = CollectionList.objects.filter(
        owner_id=user_id, status=True
    ).order_by('name')
    return render(
        request,
        'guide/user_public_collections.html',
        {'target_user': target_user, 'public_collections': public_collections},
    )


@login_required
def collection_add(request, collection_pk, post_pk):
    collection = get_object_or_404(CollectionList, pk=collection_pk)
    post = get_object_or_404(Post, pk=post_pk)
    if collection.owner != request.user:
        raise Http404
    collection.posts.add(post)
    next_url = request.GET.get('next') or request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('guide:post_detail', pk=post.pk)


@login_required
def collection_remove(request, collection_pk, post_pk):
    collection = get_object_or_404(CollectionList, pk=collection_pk)
    post = get_object_or_404(Post, pk=post_pk)
    if collection.owner != request.user:
        raise Http404
    collection.posts.remove(post)
    next_url = request.GET.get('next') or request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('guide:collection_detail', pk=collection.pk)


@login_required
def collection_delete(request, pk):
    collection = get_object_or_404(CollectionList, pk=pk)
    if collection.owner != request.user:
        raise Http404
    collection.delete()
    return redirect('guide:collection_list')
