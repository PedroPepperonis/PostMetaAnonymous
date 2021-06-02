from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, CreateView, ListView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from .forms import *
from .models import *


class HomePage(ListView):
    model = Thread
    template_name = 'PostMetaAnonymous/index.html'
    context_object_name = 'threads'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class ProfilePage(View):
    def get(self, request, url,  *args, **kwargs):
        context = {
            'title': Profile.objects.get(slug=url),
            'user': Profile.objects.get(slug=url),
            'comments': Comment.objects.filter(author__slug=url)[:5],
            'friends_request': FriendRequest.objects.all(),
        }
        return render(self.request, 'PostMetaAnonymous/profile.html', context)


class EditThread(UpdateView):
    model = Thread
    form_class = ThreadForm
    slug_url_kwarg = 'url'
    template_name = 'PostMetaAnonymous/edit_thread.html'
    success_url = reverse_lazy('threads')


class NewThread(CreateView):
    form_class = ThreadForm
    template_name = 'PostMetaAnonymous/new_thread.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def post(self, request, *args, **kwargs):
        form = ThreadForm(self.request.POST)
        if form.is_valid():
            new_thread = Thread.objects.create(
                author=self.request.user.profile,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content']
            )
            new_thread.save()
            return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новый пост'
        return context


class ShowThread(FormMixin, DetailView):
    model = Thread
    form_class = CommentForm
    template_name = 'PostMetaAnonymous/thread.html'
    slug_url_kwarg = 'url'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        thread = get_object_or_404(Thread, slug=self.kwargs['url'])
        liked = False
        if thread.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['title'] = self.get_object()
        context['liked'] = liked
        return context

    def post(self, request, url):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            new_comment = Comment.objects.create(
                author=self.request.user.profile,
                content=form.cleaned_data['content'],
                thread=Thread.objects.get(slug=url)
            )
            new_comment.save()
            return redirect(self.request.path)


class MyThreadsPage(ListView):
    model = Thread
    template_name = 'PostMetaAnonymous/user_threads.html'
    context_object_name = 'threads'

    def get_queryset(self):
        threads = Thread.objects.filter(author=self.request.user.profile)
        return threads

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои посты'
        return context


class EditPage(SuccessMessageMixin, UpdateView):
    form_class = ProfileChangeForm
    template_name = 'PostMetaAnonymous/edit_profile.html'
    slug_url_kwarg = 'url'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Данные профиля успешно обновлены')
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context


class RegisterPage(CreateView):
    form_class = RegisterForm
    template_name = 'PostMetaAnonymous/register.html'

    def post(self, request, *args, **kwargs):
        form = RegisterForm(self.request.POST)
        if form.is_valid():
            new_user = User.objects.create(
                username=form.cleaned_data['username'],
                password=make_password(form.cleaned_data['password']),
            )
            new_user.save()

            new_profile = Profile.objects.create(
                user=User.objects.get(username=form.cleaned_data['username']),
                username=form.cleaned_data['username'],
                nickname=form.cleaned_data['username'],
                slug=slugify(form.cleaned_data['username']),
                snusoman=form.cleaned_data['snusoman'],
                password=make_password(form.cleaned_data['password']),
            )
            new_profile.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect('profile', form.cleaned_data['username'])
        else:
            return render(self.request, 'PostMetaAnonymous/register.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class LoginPage(LoginView):
    form_class = LoginForm
    template_name = 'PostMetaAnonymous/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context


@login_required
def like(request, url):
    post = get_object_or_404(Thread, slug=url)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        down_user_rank(request, post.author_id)
        liked = False
    else:
        post.likes.add(request.user)
        up_user_rank(request, post.author_id)
        liked = True

    return HttpResponseRedirect(reverse('thread', args=[str(url)]))


@login_required
def comment_like(request, id):
    comment = get_object_or_404(Comment, id=id)
    liked = False
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        down_user_rank(request, comment.author_id)
        liked = False
    else:
        comment.likes.add(request.user)
        up_user_rank(request, comment.author_id)
        liked = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_post(request, url):
    thread = Thread.objects.get(slug=url)
    thread.delete()
    return redirect('threads')


@login_required
def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def up_user_rank(request, id):
    rank = Rank.objects.all()
    liked_user = get_object_or_404(Profile, id=id)
    liked_user.experience += 1
    for i in rank:
        if liked_user.experience < i.experience:
            liked_user.rank_id = i.id - 1
            break

    return liked_user.save()


@login_required
def down_user_rank(request, id):
    rank = Rank.objects.all()

    liked_user = get_object_or_404(Profile, id=id)
    liked_user.experience -= 1
    for i in rank:
        if liked_user.experience < i.experience:
            liked_user.rank_id = i.id - 1
            break

    return liked_user.save()


@login_required
def send_friend_request(request, userID):
    from_user = request.user.profile
    to_user = get_object_or_404(Profile, id=userID)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return HttpResponseRedirect(reverse('home'))
    return HttpResponse('error')


@login_required
def accept_friend_request(request, requestID):
    friend_request = get_object_or_404(FriendRequest, id=requestID)
    if friend_request.to_user == request.user.profile:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')
    return HttpResponse('friend request not accepted')
