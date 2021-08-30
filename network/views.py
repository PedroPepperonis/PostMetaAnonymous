from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import DetailView, CreateView, ListView, UpdateView
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, ProfileChangeForm, PostForm, CommentForm, GroupAdminForm, \
    GroupModeratorForm, EditPostForm
from .models import User, Post, Comment, Rank, Group, FriendRequest


def sort_posts_by_time_create(posts):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(posts) - 1):
            if posts[i].time_create < posts[i + 1].time_create:
                posts[i], posts[i + 1] = posts[i + 1], posts[i]
                swapped = True
    return posts


class HomePage(ListView):
    model = Post
    template_name = 'PostMetaAnonymous/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        groups = Group.objects.filter(followers=self.request.user)
        posts = []
        for i in range(len(groups)):
            posts += Post.objects.filter(group=groups[i])
        if len(groups) == 0:
            posts = Post.objects.all()[:5]
        sort_posts_by_time_create(posts)
        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        groups_count = Group.objects.filter(followers=self.request.user)
        groups = True
        if len(groups_count) == 0:
            groups = False
        context['groups'] = groups
        return context


class UserPage(DetailView):
    model = User
    template_name = 'PostMetaAnonymous/Profile/../templates/PostMetaAnonymous/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return User.objects.get(slug=self.kwargs['url'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, slug=self.kwargs['url'])
        is_friends = False
        if user.friends.filter(id=self.request.user.id).exists():
            is_friends = True

        friends_request_is_send = False
        friend_requests = FriendRequest.objects.filter(to_user__slug=self.kwargs['url'], from_user=self.request.user)
        if friend_requests.exists():
            friends_request_is_send = True

        context['title'] = user.nickname
        context['friends_requests'] = FriendRequest.objects.filter(to_user__slug=self.kwargs['url'])
        context['friends_request_is_send'] = friends_request_is_send
        context['is_friends'] = is_friends
        context['friends'] = user.friends.all()[:5]
        return context


class FriendsListPage(ListView):
    model = User
    template_name = 'PostMetaAnonymous/Profile/friends.html'
    context_object_name = 'user'

    def get_queryset(self, *args, **kwargs):
        user = get_object_or_404(User, slug=self.kwargs['url'])
        return user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Друзья ' + str(self.request.user)
        return context


class GroupPage(DetailView):
    model = Group
    slug_url_kwarg = 'url'
    template_name = 'PostMetaAnonymous/Group/group.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscribed = False
        group = get_object_or_404(Group, slug=self.kwargs['url'])
        if group.followers.filter(id=self.request.user.id).exists():
            subscribed = True
        admin = False
        if group.admin == self.request.user:
            admin = True
        moderator = False
        if group.moderator.filter(id=self.request.user.id).exists():
            moderator = True

        context['title'] = group.title
        context['subscribed'] = subscribed
        context['admin'] = admin
        context['moderator'] = moderator
        return context


class GroupEdit(UserPassesTestMixin, UpdateView):
    model = Group
    slug_url_kwarg = 'url'
    template_name = 'PostMetaAnonymous/Group/edit.html'

    def test_func(self):
        post = get_object_or_404(Group, slug=self.kwargs['url'])
        if post.admin == self.request.user:
            self.form_class = GroupAdminForm
            return True
        if post.moderator.filter(id=self.request.user.id):
            self.form_class = GroupModeratorForm
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('group', args=[self.kwargs['url']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = get_object_or_404(Group, slug=self.kwargs['url'])
        context['title'] = 'Редактирование группы ' + str(group.title)
        return context


class EditPost(UpdateView):
    model = Post
    form_class = EditPostForm
    slug_url_kwarg = 'url'
    template_name = 'PostMetaAnonymous/Posts/edit.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['url'])
        context['title'] = 'Редактирование поста ' + str(post.title)
        return context


class NewPost(CreateView):
    form_class = PostForm
    template_name = 'PostMetaAnonymous/Posts/new.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        return PostForm(self.request.user)

    def post(self, request, *args, **kwargs):
        form = PostForm(self.request.user, self.request.POST)
        if form.is_valid():
            group = get_object_or_404(Group, title=form.cleaned_data['group'].title)
            post = Post.objects.create(
                author=self.request.user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                group=form.cleaned_data['group']
            )
            group.posts.add(post)
            post.save()
            group.save()

            return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новый пост'
        return context


class ShowPost(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'PostMetaAnonymous/Posts/post.html'
    slug_url_kwarg = 'url'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['url'])
        context['title'] = self.get_object()
        context['comments'] = Comment.objects.filter(post=post)
        return context

    def post(self, request, group, url):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            new_comment = Comment.objects.create(
                author=self.request.user,
                content=form.cleaned_data['content'],
                post=Post.objects.get(slug=self.kwargs['url'])
            )
            new_comment.save()
            return redirect(self.request.path)


class UserPosts(ListView):
    model = Post
    template_name = 'PostMetaAnonymous/Posts/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Посты ' + str(self.request.user.nickname)
        return context


class EditPage(UpdateView):
    form_class = ProfileChangeForm
    template_name = 'PostMetaAnonymous/Profile/edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    # return reverse_lazy('group', args=[self.kwargs['url']])
    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.slug])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context


class RegisterPage(CreateView):
    form_class = RegisterForm
    template_name = 'PostMetaAnonymous/Utils/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class LoginPage(LoginView):
    form_class = LoginForm
    template_name = 'PostMetaAnonymous/Utils/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context


class SearchPage(View):
    def get(self, request):
        print(self.request.GET.get('query'))
        posts = Post.objects.filter(title__icontains=self.request.GET.get('query'))
        groups = Group.objects.filter(title__icontains=self.request.GET.get('query'))
        users = User.objects.filter(nickname__icontains=self.request.GET.get('query'))
        context = {
            'posts': posts,
            'groups': groups,
            'users': users,
        }
        return render(request, 'PostMetaAnonymous/Utils/search.html', context=context)

    def get_queryset(self):
        posts = Post.objects.filter(title__icontains=self.request.GET.get('query'))
        groups = Group.objects.filter(title__icontains=self.request.GET.get('query'))
        users = User.objects.filter(nickname__icontains=self.request.GET.get('query'))
        return posts


# система лайков
def post_like(request):
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        down_user_rank(request, post.author_id)
        return JsonResponse({'likes': post.get_likes_count(), 'dislikes': post.get_dislikes_count()}, status=200)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    if not post.likes.filter(id=request.user.id).exists():
        post.likes.add(request.user)
        up_user_rank(request, post.author_id)
    return JsonResponse({'likes': post.get_likes_count(), 'dislikes': post.get_dislikes_count()}, status=200)


def post_dislike(request):
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        up_user_rank(request, post.author_id)
        return JsonResponse({'likes': post.get_likes_count(), 'dislikes': post.get_dislikes_count()}, status=200)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    if not post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.add(request.user)
        down_user_rank(request, post.author_id)
    return JsonResponse({'likes': post.get_likes_count(), 'dislikes': post.get_dislikes_count()}, status=200)


def comment_like(request, user_id):
    comment = get_object_or_404(Comment, id=user_id)
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


def delete_comment(request):
    comment_id = request.GET.get('comment_id')
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return JsonResponse({'message': 'Удалено'}, status=200)


def delete_post(request, unique_id):
    post = Post.objects.get(unique_id=unique_id)
    if post.delete():
        return JsonResponse({'message': 'Пост успешно удален'}, status=200)
    return JsonResponse({'message': 'Не удалось удалить пост'}, status=503)


# логаут
def logout_user(request):
    logout(request)
    return redirect('home')


# система рангов
def up_user_rank(request, user_id):
    rank = Rank.objects.all()
    liked_user = get_object_or_404(User, id=user_id)
    liked_user.experience += 1
    for i in rank:
        if liked_user.experience < i.experience:
            liked_user.rank_id = i.id - 1
            break

    return liked_user.save()


def down_user_rank(request, user_id):
    rank = Rank.objects.all()

    liked_user = get_object_or_404(User, id=user_id)
    liked_user.experience -= 1
    for i in rank:
        if liked_user.experience < i.experience:
            liked_user.rank_id = i.id - 1
            break

    return liked_user.save()


# система друзей
def send_friend_request(request):
    user_id = request.GET.get('user_id')
    from_user = get_object_or_404(User, id=request.user.id)
    to_user = get_object_or_404(User, id=user_id)
    FriendRequest.objects.create(
        from_user=from_user,
        to_user=to_user,
    ).save()
    return JsonResponse({'message': 'Success'}, status=200)


def accept_friend_request(request):
    request_id = request.GET.get('request_id')
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    from_user = get_object_or_404(User, id=friend_request.from_user.id)
    to_user = get_object_or_404(User, id=friend_request.to_user.id)
    from_user.friends.add(to_user)
    to_user.friends.add(from_user)
    friend_request.delete()
    return JsonResponse({'message': 'Success'}, status=200)


def decline_friend_request(request):
    request_id = request.GET.get('request_id')
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    friend_request.delete()
    return JsonResponse({'message': 'Success'})


def delete_friend(request):
    user_id = request.GET.get('user_id')
    from_user = get_object_or_404(User, id=request.user.id)
    to_user = get_object_or_404(User, id=user_id)
    from_user.friends.remove(to_user)
    to_user.friends.remove(from_user)
    return JsonResponse({'message': 'Success'}, status=200)


# группы
def subscribe_to_group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    user = get_object_or_404(User, id=request.user.id)
    user.groups.add(group)
    group.followers.add(request.user)
    return JsonResponse({'message': 'Успешно'}, status=200)


def unsubscribe_from_group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    user = get_object_or_404(User, id=request.user.id)
    user.groups.remove(group)
    group.followers.remove(request.user)
    return JsonResponse({'message': 'Успешно'}, status=200)
