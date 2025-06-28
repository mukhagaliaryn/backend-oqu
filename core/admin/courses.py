from django.contrib import admin
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdminMixin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from core.forms import CourseAdminForm
from core.models import Subcategory, Chapter, Lesson, Category, Course, Language


# Category admin
# ----------------------------------------------------------------------------------------------------------------------
# SubCategory
class SubCategoryInline(TranslationTabularInline):
    model = Subcategory
    extra = 1
    prepopulated_fields = {'slug': ('name_en', )}


# Category
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name_en', )}
    inlines = (SubCategoryInline, )


# Course admin
# ----------------------------------------------------------------------------------------------------------------------
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )


# Chapter
class ChapterTable(TranslationTabularInline):
    model = Chapter
    extra = 0


# Lesson
class LessonTable(TranslationTabularInline):
    model = Lesson
    readonly_fields = ('view_link',)
    fields = ('title', 'chapter', 'duration', 'access', 'order', 'view_link', )
    extra = 0

    # Detail view
    def view_link(self, obj):
        if obj.pk:
            url = reverse('admin:core_lesson_change', args=[obj.pk])
            return format_html('<a href="{}" class="lesson-view-link">Толығырақ</a>', url)
        return "-"

    view_link.short_description = _('Lesson link')

    # Chapter choice
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "chapter":
            course_id = request.resolver_match.kwargs.get('object_id')
            if course_id:
                kwargs['queryset'] = Chapter.objects.filter(course_id=course_id)
            else:
                kwargs['queryset'] = Chapter.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Course
class CourseAdmin(SummernoteModelAdminMixin, TranslationAdmin):
    form = CourseAdminForm
    list_display = ('name', 'category', 'sub_category', 'last_update', )
    list_filter = ('category', 'sub_category', )
    search_fields = ('name', 'category', 'sub_category', )
    filter_horizontal = ('authors', 'languages', )
    summernote_fields = ('description', )
    inlines = (ChapterTable, LessonTable, )

    class Media:
        js = (static('scripts/category_choice.js'), )


# registrations
# ----------------------------------------------------------------------------------------------------------------------
admin.site.register(Category, CategoryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Course, CourseAdmin)
