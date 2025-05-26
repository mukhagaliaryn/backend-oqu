from unicodedata import category

from django.shortcuts import get_object_or_404
from rest_framework import views, permissions, status
from rest_framework.response import Response
from apps.platform.main.serializers.publics import MainCoursesSerializer, MainBlogsSerializer, FAQSerializer, \
    MainBlogSerializer, MainBlogCategorySerializer
from core.models import Course, Blog, FAQ, BlogCategory


# Main API view
# ----------------------------------------------------------------------------------------------------------------------
class MainAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    def get(self, request):
        courses = Course.objects.filter()[:5]
        blogs = Blog.objects.filter()[:5]
        faqs = FAQ.objects.filter()[:6]

        courses_serializers = MainCoursesSerializer(courses, many=True, context={'request': request})
        blogs_serializers = MainBlogsSerializer(blogs, many=True, context={'request': request})
        faqs_serializers = FAQSerializer(faqs, many=True)

        context = {
            'courses': courses_serializers.data,
            'blogs': blogs_serializers.data,
            'faqs': faqs_serializers.data
        }
        return Response(context, status=status.HTTP_200_OK)


# Blog API view
# ----------------------------------------------------------------------------------------------------------------------
# List
class BlogAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    def get(self, request):
        blogs = Blog.objects.filter()
        categories = BlogCategory.objects.all()

        blogs_serializers = MainBlogsSerializer(blogs, many=True, context={'request': request})
        category_serializers = MainBlogCategorySerializer(categories, many=True)
        context = {
            'blogs': blogs_serializers.data,
            'categories': category_serializers.data
        }
        return Response(context, status=status.HTTP_200_OK)


# Category detail
class BlogCategoryDetailAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    def get(self, request, slug):
        blog_category = get_object_or_404(BlogCategory, slug=slug)
        categories = BlogCategory.objects.all()
        blogs = Blog.objects.filter(category=blog_category)

        category_serializers = MainBlogCategorySerializer(blog_category, partial=True)
        categories_serializers = MainBlogCategorySerializer(categories, many=True)
        blogs_serializers = MainBlogsSerializer(blogs, many=True, context={'request': request})
        context = {
            'category': category_serializers.data,
            'categories': categories_serializers.data,
            'blogs': blogs_serializers.data,
        }
        return Response(context, status=status.HTTP_200_OK)


# Blog detail
class BlogDetailAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        blog_serializers = MainBlogSerializer(blog, partial=True, context={'request': request})
        context = {
            'blog': blog_serializers.data,
        }
        return Response(context, status=status.HTTP_200_OK)


# Course API view
# ----------------------------------------------------------------------------------------------------------------------
# detail
class CourseDetailAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        course_serializers = MainCoursesSerializer(course, partial=True, context={'request': request})
        context = {
            'course': course_serializers.data,
        }
        return Response(context, status=status.HTTP_200_OK)
