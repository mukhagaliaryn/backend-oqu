from rest_framework import serializers
from core.models import Course, Subcategory, BlogCategory, Blog, FAQ


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


# CourseDetail
class MainCourseDetailSerializer(serializers.ModelSerializer):
    sub_category = MainSubCategorySerializer()

    class Meta:
        model = Course
        fields = '__all__'


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
        fields = ('id', 'title', 'category', 'shortcut', 'created_at', )


# Blog
class MainBlogSerializer(serializers.ModelSerializer):
    category = MainBlogCategorySerializer()

    class Meta:
        model = Blog
        fields = '__all__'


# FAQs
# ----------------------------------------------------------------------------------------------------------------------
class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = ('id', 'title', 'content', 'content', 'order', )
