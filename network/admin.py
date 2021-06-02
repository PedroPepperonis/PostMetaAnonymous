from django.contrib import admin
from django.contrib.auth.models import User
from .models import *


class SnusomanAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name',)}


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'slug': ('title',)}


class RankAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Profile)
admin.site.register(Snusoman, SnusomanAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment)
#admin.site.register(Reply)
admin.site.register(Rank, RankAdmin)
admin.site.register(FriendRequest)
