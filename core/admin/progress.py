from django.contrib import admin
from core.models import UserChapter, UserLesson, UserCourse, UserVideo, UserText


# UserCourse admin
# ----------------------------------------------------------------------------------------------------------------------
# UserChapter
class UserChapterTable(admin.TabularInline):
    model = UserChapter
    extra = 0


# UserLesson
class UserLessonTable(admin.TabularInline):
    model = UserLesson
    extra = 0


# UserCourse
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'is_completed', )
    list_filter = ('user', 'course', 'is_completed', )
    search_fields = ('course', 'user', )

    inlines = [UserChapterTable, UserLessonTable]


# UserCourse admin
# ----------------------------------------------------------------------------------------------------------------------
# UserVideo
class UserVideoInline(admin.TabularInline):
    model = UserVideo
    extra = 0


# UserVideo
class UserTextInline(admin.TabularInline):
    model = UserText
    extra = 0


# UserLesson
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'user_course', 'is_completed', )

    inlines = [UserVideoInline, UserTextInline]


# registrations
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(UserLesson, UserLessonAdmin)
