from django.urls import path
from apps.platform.workspace.views import main, course


urlpatterns = [
    path('', main.workspace, name='workspace'),
    path('resources/', main.resources, name='resources'),
    path('course/<pk>/', main.course_detail, name='course_detail'),
    path('course/<int:pk>/create/', main.create_user_course_handler, name='create_user_course'),

    # user course urls...
    path('user/course/<user_course_pk>/chapter/<user_chapter_pk>/lesson/<user_lesson_pk>/',
         course.user_course_lesson_view, name='user_course_lesson'
    ),
]
