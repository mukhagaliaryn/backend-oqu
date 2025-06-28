from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from core.models import UserChapter, UserLesson, UserCourse, UserVideo, UserText, UserTest, UserAnswer


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
    readonly_fields = ('view_link',)
    fields = ('user', 'lesson', 'score', 'status', 'is_completed', 'view_link', )

    # Detail view
    def view_link(self, obj):
        if obj.pk:
            url = reverse('admin:core_userlesson_change', args=[obj.pk])
            return format_html('<a href="{}" class="lesson-view-link">Толығырақ</a>', url)
        return "-"

    view_link.short_description = _('User lesson link')


# UserCourse
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'score', 'is_completed', )
    list_filter = ('user', 'course', 'is_completed', )
    search_fields = ('course', 'user', )

    inlines = [UserChapterTable, UserLessonTable]


# UserCourse admin
# ----------------------------------------------------------------------------------------------------------------------
# UserText
class UserTextInline(admin.TabularInline):
    model = UserText
    extra = 0


# UserVideo
class UserVideoInline(admin.TabularInline):
    model = UserVideo
    extra = 0


# UserTest
class UserTestInline(admin.TabularInline):
    model = UserTest
    extra = 0
    readonly_fields = ('view_link',)
    fields = ('user', 'test', 'score', 'is_completed', 'view_link', )

    # Detail view
    def view_link(self, obj):
        if obj.pk:
            url = reverse('admin:core_usertest_change', args=[obj.pk])
            return format_html('<a href="{}" class="lesson-view-link">Толығырақ</a>', url)
        return "-"

    view_link.short_description = _('User test link')


# UserLesson
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'user_course', 'is_completed', )

    inlines = [UserTextInline, UserVideoInline, UserTestInline ]


# UserTest admin
# ----------------------------------------------------------------------------------------------------------------------
# UserAnswer
class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0


# UserTest
class UserTestAdmin(admin.ModelAdmin):
    list_display = ('user_lesson', 'test', 'user', 'score', 'is_completed', )
    list_filter = ('user', 'test', 'is_completed', )
    inlines = [UserAnswerInline]


# registrations
# ----------------------------------------------------------------------------------------------------------------------
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(UserLesson, UserLessonAdmin)
admin.site.register(UserTest, UserTestAdmin)
