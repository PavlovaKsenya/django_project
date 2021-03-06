from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from blog.forms import AddPostForm, RegisterUserForm, LoginUserForm
from blog.models import *
from blog.utils import DataMixin

menu = [{'title': 'Лучшие рецепты мира', 'url_name': 'home'},
        {'title': 'Добавить статью', 'url_name': 'addpage'},
        # {'title': 'Войти', 'url_name': 'login'}
       ]

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "blog/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "blog/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = "blog/addpage.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавление рецепта'
        return context



class PostCategory(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = "blog/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['post']
        return context


class BlogHome(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    extra_context = {'title': 'Главная страница'}


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True)[:5]


def categories(request, cat):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{cat}</p>")


def archive(request, year):
    if int(year) > 2022:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exeption):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


