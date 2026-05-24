from django.contrib import admin
from .models import Community, Post, Comment

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ["name", "created_by", "created_at"]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "community", "upvotes", "created_at"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "post", "created_at"]
