from django.urls import path
from .views import *


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('login/', LoginPage.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),

    path('profile/<slug:url>/', UserPage.as_view(), name='profile'),
    path('profile/<slug:url>/threads/', UserThreads.as_view(), name='threads'),
    path('profile/<slug:url>/edit_profile/', EditPage.as_view(), name='edit_profile'),
    path('profile/<slug:url>/friends/', FriendsListPage.as_view(), name='friends'),

    path('new_thread/', NewThread.as_view(), name='new_thread'),
    path('thread/<slug:url>/', login_required(ShowThread.as_view()), name='thread'),
    path('edit_thread/<slug:url>/', EditThread.as_view(), name='edit_thread'),
    path('delete_thread/<slug:url>', delete_post, name='delete_thread'),

    path('delete_comment/<int:id>', delete_comment, name='delete_comment'),
    path('like/<slug:url>', like, name='thread_like'),
    path('comment_like/<int:id>', comment_like, name='comment_like'),

    path('add_friend/<int:userID>', send_friend_request, name='send_friend_request'),
    path('accept_friend/<int:requestID>', accept_friend_request, name='accept_friend_request'),
    path('decline_friend/<int:requestID>', decline_friend_request, name='decline_request'),
    path('delete_friend/<int:userID>', delete_friend, name='delete_friend'),

    path('search/', SearchPage.as_view(), name='search'),
]
