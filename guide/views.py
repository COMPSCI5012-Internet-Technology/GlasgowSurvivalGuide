from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Post
from .forms import PostForm

from guide.forms import EmailLoginForm, RegisterForm


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
    if request.user.is_authenticated:
        post_list_qs = Post.objects.filter(
            Q(status=True) | Q(author=request.user)
        ).order_by('-created_at')
    else:
        post_list_qs = Post.objects.filter(status=True).order_by('-created_at')
    return render(request, 'guide/post_list.html', {'post_list': post_list_qs})





def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.status and (
        not request.user.is_authenticated or request.user != post.author
    ):
        raise Http404
    return render(request, 'guide/post_detail.html', {'post': post})