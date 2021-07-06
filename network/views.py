from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import DetailView, CreateView, ListView, UpdateView
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from itertools import chain

from friendship.models import Friend, FriendshipRequest

from .forms import RegisterForm, LoginForm, ProfileChangeForm, ThreadForm, CommentForm
from .models import User, Thread, Comment, Rank


class HomePage(ListView):
    model = Thread
    template_name = 'PostMetaAnonymous/index.html'
    context_object_name = 'threads'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class UserPage(DetailView):
    model = User
    template_name = 'PostMetaAnonymous/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return User.objects.get(slug=self.kwargs['url'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, slug=self.kwargs['url'])
        context['title'] = self.request.user.nickname
        context['comments'] = Comment.objects.filter(author=self.request.user)[:5]
        context['friends'] = Friend.objects.friends(user)
        context['friend_requests'] = Friend.objects.unread_requests(self.request.user)
        return context


class FriendsListPage(ListView):
    model = Friend
    template_name = 'PostMetaAnonymous/friends_list.html'
    context_object_name = 'friends'

    def get_queryset(self, *args, **kwargs):
        user = get_object_or_404(User, slug=self.kwargs['url'])
        return Friend.objects.friends(user)


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
        return self.request.user

    def post(self, request, *args, **kwargs):
        form = ThreadForm(self.request.POST)
        if form.is_valid():
            new_thread = Thread.objects.create(
                author=self.request.user,
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
                author=self.request.user,
                content=form.cleaned_data['content'],
                thread=Thread.objects.get(slug=url)
            )
            new_comment.save()
            return redirect(self.request.path)


class UserThreads(ListView):
    model = Thread
    template_name = 'PostMetaAnonymous/user_threads.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return Thread.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои посты'
        return context


class EditPage(UpdateView):
    form_class = ProfileChangeForm
    template_name = 'PostMetaAnonymous/edit_profile.html'
    slug_url_kwarg = 'url'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return JsonResponse({'message': 'Данные профиля успешно обновлены'}, status=200)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context


class RegisterPage(CreateView):
    form_class = RegisterForm
    template_name = 'PostMetaAnonymous/register.html'
    success_url = reverse_lazy('login')

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


class SearchPage(ListView):
    template_name = 'PostMetaAnonymous/search.html'
    context_object_name = 'results'

    def get_queryset(self):
        threads = Thread.objects.filter(title__icontains=self.request.GET.get('query'))
        users = User.objects.filter(nickname__icontains=self.request.GET.get('query'))
        results = chain(users, threads)
        return results

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.GET.get('query')
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
    liked_user = get_object_or_404(User, id=id)
    liked_user.experience += 1
    for i in rank:
        if liked_user.experience < i.experience:
            liked_user.rank_id = i.id - 1
            break

    return liked_user.save()


@login_required
def down_user_rank(request, id):
    rank = Rank.objects.all()

    liked_user = get_object_or_404(User, id=id)
    liked_user.experience -= 1
    for i in rank:
        if liked_user.experience < i.experience:
            liked_user.rank_id = i.id - 1
            break

    return liked_user.save()


@login_required
def send_friend_request(request, userID):
    to_user = get_object_or_404(User, id=userID)
    Friend.objects.add_friend(request.user, to_user)
    return JsonResponse({'success': 'Success'}, status=200)


@login_required
def accept_friend_request(request, requestID):
    friend_request = FriendshipRequest.objects.get(id=requestID)
    friend_request.accept()
    return redirect('home')


@login_required
def decline_friend_request(request, requestID):
    friend_request = FriendshipRequest.objects.get(id=requestID)
    friend_request.cancel()
    return redirect('home')


@login_required
def delete_friend(request, userID):
    Friend.objects.remove_friend(userID, request.user)
    return redirect('home')
