from django.contrib import admin
from django_summernote.admin import SummernoteModelAdminMixin
from modeltranslation.admin import TranslationAdmin
from core.models import Lesson, Question, Answer, Video, Text, Test


# Lesson admin
# ----------------------------------------------------------------------------------------------------------------------
# Video
class VideoInline(admin.TabularInline):
    model = Video
    extra = 0


# Text
class TextInline(SummernoteModelAdminMixin, admin.TabularInline):
    model = Text
    extra = 0


# Test
class TestInline(admin.TabularInline):
    model = Test
    extra = 0


# Lesson
class LessonAdmin(SummernoteModelAdminMixin, TranslationAdmin):
    list_display = ('title', 'course', 'chapter', 'last_update', 'access', 'order', )
    list_filter = ('course', 'chapter', 'access', )
    inlines = [TextInline, VideoInline, TestInline ]


# Test admin
# ----------------------------------------------------------------------------------------------------------------------
# Question
class QuestionInline(SummernoteModelAdminMixin, admin.TabularInline):
    model = Question
    extra = 0


# Test
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'order', )
    list_filter = ('lesson', )
    inlines = [QuestionInline, ]



# Question admin
# ----------------------------------------------------------------------------------------------------------------------
# Answer
class AnswerInline(SummernoteModelAdminMixin, admin.TabularInline):
    model = Answer
    extra = 0


# Question
class QuestionAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    list_display = ('test', 'order', )
    list_filter = ('test', )
    inlines = [AnswerInline, ]


# registrations
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
