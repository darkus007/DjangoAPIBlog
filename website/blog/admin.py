from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_display_links = ('title',)
    search_fields = ('title',)


admin.site.register(Post, PostAdmin)
