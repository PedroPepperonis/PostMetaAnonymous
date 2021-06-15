from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class ProfileAdmin(UserAdmin):
    list_display = ('email', 'username', 'nickname', 'is_admin', 'is_staff')
    readonly_fields = ('password', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class SnusomanAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name',)}


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'slug': ('title',)}


class RankAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Snusoman, SnusomanAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment)
admin.site.register(Rank, RankAdmin)
admin.site.register(FriendRequest)
