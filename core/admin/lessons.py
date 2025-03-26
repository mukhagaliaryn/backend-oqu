from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from core.models import Lesson, Video


# Lesson admin
# ----------------------------------------------------------------------------------------------------------------------
# Video
class VideoTab(admin.TabularInline):
    model = Video
    extra = 0


# Lesson
class LessonAdmin(TranslationAdmin):
    list_display = ('title', 'course', 'chapter', 'last_update', 'access', 'order', )
    list_filter = ('course', 'chapter', 'access', )
    inlines = [VideoTab ]


# registrations
admin.site.register(Lesson, LessonAdmin)
