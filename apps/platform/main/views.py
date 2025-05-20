from rest_framework import views, permissions, status
from rest_framework.response import Response
from apps.platform.main.serializers.publics import MainCoursesSerializer, MainBlogsSerializer
from core.models import Course, Blog


# Main API view
# ----------------------------------------------------------------------------------------------------------------------
class MainAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    def get(self, request):
        courses = Course.objects.filter()[:5]
        blogs = Blog.objects.filter()[:5]

        courses_serializers = MainCoursesSerializer(courses, many=True, context={'request': request})
        blogs_serializers = MainBlogsSerializer(blogs, many=True, context={'request': request})

        context = {
            'courses': courses_serializers.data,
            'blogs': blogs_serializers.data
        }
        return Response(context, status=status.HTTP_200_OK)
