from modeltranslation.translator import translator, TranslationOptions
from core.models import Category, Subcategory, Course, Chapter, Lesson


# Category translation
# ----------------------------------------------------------------------------------------------------------------------
# Category
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )

# Subcategory
class SubcategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


# Course translation
# ----------------------------------------------------------------------------------------------------------------------
# Course
class CourseTranslationOptions(TranslationOptions):
    fields = ('name', 'about', 'description', )


# Chapter
class ChapterTranslationOptions(TranslationOptions):
    fields = ('name', )


# translations
translator.register(Category, CategoryTranslationOptions)
translator.register(Subcategory, SubcategoryTranslationOptions)
translator.register(Course, CourseTranslationOptions)
translator.register(Chapter, ChapterTranslationOptions)
