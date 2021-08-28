from django.contrib import admin
from .models import User, Snusoman, Post, Group, Comment, Rank, FriendRequest


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'nickname', 'is_admin', 'is_staff')
    readonly_fields = ('password', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class SnusomanAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'group', 'time_create')
    prepopulated_fields = {'slug': ('title',)}


class RankAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(User, UserAdmin)
admin.site.register(Snusoman, SnusomanAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Rank, RankAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(FriendRequest)

