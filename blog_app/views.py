from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import UserForm, PostForm, CommentForm

################## Views...

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = user.password
            try:
                validate_password(password, user)
            except ValidationError as e:
                form.add_error('password',e)
            else:
                user.set_password(password)
                user.save()
                return redirect('blog_app:login')
    else:
        form = UserForm()
    return render(request, 'blog_app/register.html', {'form':form})

def user_login(request):
    error = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('blog_app:index')
            else:
                error += "Inactive User, please contact admin."
        else:
            error += "Invalid login details."
    return render(request, 'blog_app/login.html', {'error':error})

@login_required
def user_logout(request):
    logout(request)
    return redirect('blog_app:index')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_app:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog_app/post_form.html', {'form':form})
    

##################
##################

class IndexView(TemplateView):
    template_name = 'blog_app/index.html'

class PostListView(ListView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog_app:post_list'
    model = Post
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, publish_date__isnull=True).order_by('-create_date')
    template_name = 'blog_app/drafts.html'

class PostDetailView(DetailView):
    model = Post

# class CreatePost(LoginRequiredMixin, CreateView):
#     login_url = '/login/'
#     redirect_field_name = 'blog_app:index'
#     model = Post
#     form_class = PostForm

class UpdatePost(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog_app:index'
    model = Post
    form_class = PostForm

class DeletePost(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'blog_app:index'
    model = Post
    success_url = reverse_lazy('blog_app:post_list')

#####################
#####################

@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog_app:post_detail', pk=pk)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        author = request.POST.get('author')
        text = request.POST.get('text')
        comment = Comment(post=post, author=author, text=text)
        comment.save()
    return redirect('blog_app:post_detail', pk=pk)

# @login_required
# def comment_approve(request, )

