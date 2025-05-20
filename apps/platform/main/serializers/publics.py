from rest_framework import serializers
from core.models import Course, Subcategory, BlogCategory, Blog


# Course serializers
# ----------------------------------------------------------------------------------------------------------------------
class MainSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', )


# Courses
class MainCoursesSerializer(serializers.ModelSerializer):
    sub_category = MainSubCategorySerializer()

    class Meta:
        model = Course
        fields = ('id', 'name', 'sub_category', 'poster', )


# Blog serializers
# ----------------------------------------------------------------------------------------------------------------------
# Category
class MainBlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ('id', 'name', 'slug')


# Blogs
class MainBlogsSerializer(serializers.ModelSerializer):
    category = MainBlogCategorySerializer()

    class Meta:
        model = Blog
        fields = ('id', 'title', 'category', 'content', 'created_at')