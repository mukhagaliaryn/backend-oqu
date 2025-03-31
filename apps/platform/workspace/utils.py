from core.models import UserCourse, UserChapter, UserLesson, UserVideo, UserText, UserTest, UserAnswer


# Update user progress for course
# ----------------------------------------------------------------------------------------------------------------------
def update_user_progress_for_course(course):
    user_courses = UserCourse.objects.filter(course=course).select_related('user')

    chapters = course.chapters.all()
    lessons = course.lessons.all()

    for uc in user_courses:
        user = uc.user

        for chapter in chapters:
            UserChapter.objects.get_or_create(user=user, chapter=chapter, user_course=uc)

        for lesson in lessons:
            user_lesson, _ = UserLesson.objects.get_or_create(user=user, lesson=lesson, user_course=uc)

            if hasattr(lesson, 'video'):
                UserVideo.objects.get_or_create(user=user, user_lesson=user_lesson, video=lesson.video)

            if hasattr(lesson, 'text'):
                UserText.objects.get_or_create(user=user, user_lesson=user_lesson, text=lesson.text)

            if hasattr(lesson, 'test'):
                UserTest.objects.get_or_create(user=user, user_lesson=user_lesson, test=lesson.test)
