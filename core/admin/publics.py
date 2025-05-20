from django.contrib import admin
from core.models import Blog, BlogCategory
from django_summernote.admin import SummernoteModelAdminMixin


# Blog admin
# ----------------------------------------------------------------------------------------------------------------------
# Category
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )


# Blog
class BlogAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', )


# registers
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Blog, BlogAdmin)
