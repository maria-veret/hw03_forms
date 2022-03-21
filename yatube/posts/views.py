from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Post, Group, User
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request: HttpRequest) -> HttpResponse:
    """Функция для главной страницы.
    """
    template = 'posts/index.html'
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    """Функция для записей сообщества.
    """
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Записи сообщества {group}'
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def profile(request: HttpRequest, username: str) -> HttpResponse:
    """Функция для профайла пользователя"""
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
    count_posts = author.posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Профайл пользователя {author}'
    context = {
        'author': author,
        'posts': posts,
        'count_posts': count_posts,
        'page_obj': page_obj,
        'title': title,

    }
    return render(request, template, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """Функция для просмотра записи"""
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    group = post.group
    author = post.author
    count_posts = author.posts.count()
    title = f'Пост {post.text[:30]}'
    context = {
        'post': post,
        'group': group,
        'count_posts': count_posts,
        'title': title,
    }
    return render(request, template, context)


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    """Функция для публикации постов.
    """
    template = 'posts/create_post.html'
    title = f'Создание поста'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = datetime.now()
            post.save()
            return redirect('posts:profile', request.user)
        else:
            context = {
                'form': form,
                'title': title,
            }
            return render(request, template, context)
    else:
        form = PostForm()
        context = {
            'form': form,
            'title': title,
        }
        return render(request, template, context)


@login_required
def post_edit(request: HttpRequest, post_id: int) -> HttpResponse:
    """Функция для редактирования постов.
    """
    template = 'posts/update_post.html'
    post = get_object_or_404(Post, id=post_id, author=request.user)
    title = f'Редактрирование поста {post.id}'
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = datetime.now()
            post.save()
            return redirect('posts:post_detail', post.id)
        else:
            context = {
                'form': form,
                'is_edit': True,
                'title': title,
            }
            return render(request, template, context)
    else:
        form = PostForm(instance=post)
        context = {
            'form': form,
            'is_edit': True,
            'post': post,
            'title': title,
        }
        return render(request, template, context)
