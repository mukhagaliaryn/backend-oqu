from modeltranslation.translator import register, TranslationOptions
from core.models import Category, Subcategory, Course, Chapter


# Category translation
# ----------------------------------------------------------------------------------------------------------------------
# Category
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )

# Subcategory
@register(Subcategory)
class SubcategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


# Course translation
# ----------------------------------------------------------------------------------------------------------------------
# Course
@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('name', 'about', 'description', )


# Chapter
@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('name', )
