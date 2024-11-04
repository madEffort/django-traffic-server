from django.contrib import admin
from .models import Board, Post


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
