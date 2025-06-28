from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdminMixin
from modeltranslation.admin import TranslationAdmin
from core.models import Lesson, Question, Answer, Video, Text, Test, LessonDocs


# Lesson admin
# ----------------------------------------------------------------------------------------------------------------------
# Lesson docs
class LessonDocsInline(admin.TabularInline):
    model = LessonDocs
    extra = 0


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
    readonly_fields = ('view_link',)
    fields = ('title', 'description', 'order', 'view_link', )

    # Detail view
    def view_link(self, obj):
        if obj.pk:
            url = reverse('admin:core_test_change', args=[obj.pk])
            return format_html('<a href="{}" class="lesson-view-link">Толығырақ</a>', url)
        return "-"

    view_link.short_description = _('Test link')


# Lesson
class LessonAdmin(SummernoteModelAdminMixin, TranslationAdmin):
    list_display = ('title', 'course', 'chapter', 'last_update', 'access', 'order', )
    list_filter = ('course', 'chapter', 'access', )
    inlines = [LessonDocsInline, TextInline, VideoInline, TestInline ]


# Test admin
# ----------------------------------------------------------------------------------------------------------------------
# Question
class QuestionInline(SummernoteModelAdminMixin, admin.TabularInline):
    model = Question
    extra = 0
    readonly_fields = ('view_link',)
    fields = ('text', 'order', 'view_link', )

    # Detail view
    def view_link(self, obj):
        if obj.pk:
            url = reverse('admin:core_question_change', args=[obj.pk])
            return format_html('<a href="{}" class="lesson-view-link">Толығырақ</a>', url)
        return "-"

    view_link.short_description = _('Question link')


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
    list_display = ('pk', 'test', 'order', )
    list_filter = ('test', )
    list_display_links = ('test', )
    inlines = [AnswerInline, ]


# registrations
# ----------------------------------------------------------------------------------------------------------------------
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
