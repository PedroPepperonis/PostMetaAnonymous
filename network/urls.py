from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import *


urlpatterns = [
    path('', login_required(HomePage.as_view()), name='home'),
    path('login/', LoginPage.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', login_required(logout_user), name='logout'),

    path('profile/edit/', login_required(EditPage.as_view()), name='edit_profile'),
    path('profile/<slug:url>/', login_required(UserPage.as_view()), name='profile'),
    path('profile/<slug:url>/posts/', login_required(UserPosts.as_view()), name='posts'),
    path('profile/<slug:url>/friends/', FriendsListPage.as_view(), name='friends'),

    path('new_post/', login_required(NewPost.as_view()), name='new_post'),
    path('post/<str:group>/<slug:url>/', login_required(ShowPost.as_view()), name='post'),
    path('edit_post/<slug:url>/', login_required(EditPost.as_view()), name='edit_post'),
    path('delete_post/<str:unique_id>', login_required(delete_post), name='delete_post'),

    path('group/<slug:url>', login_required(GroupPage.as_view()), name='group'),
    path('group/<slug:url>/edit/', login_required(GroupEdit.as_view()), name='edit_group'),
    path('group/subscribe/<slug:group_slug>', login_required(subscribe_to_group), name='subscribe_to_group'),
    path('group/unsubscribe/<slug:group_slug>', login_required(unsubscribe_from_group), name='unsubscribe_from_group'),

    path('delete_comment/', login_required(delete_comment), name='delete_comment'),
    path('like_post/', login_required(post_like), name='like_post'),
    path('dislike_post/', login_required(post_dislike), name='dislike_post'),
    path('comment_like/<int:id>', login_required(comment_like), name='comment_like'),

    path('send_friend_request/', login_required(send_friend_request), name='send_friend_request'),
    path('delete_friend/', login_required(delete_friend), name='delete_friend'),
    path('accept_friend_request/', login_required(accept_friend_request), name='accept_friend_request'),
    path('decline_friend_request/', login_required(decline_friend_request), name='decline_friend_request'),

    path('search/', login_required(SearchPage.as_view()), name='search'),
]
