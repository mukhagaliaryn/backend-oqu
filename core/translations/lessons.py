from modeltranslation.translator import translator, TranslationOptions
from core.models import Lesson


# Lesson translation
# ----------------------------------------------------------------------------------------------------------------------
# Lesson
class LessonTranslationOptions(TranslationOptions):
    fields = ('title', 'about', )


# translations
translator.register(Lesson, LessonTranslationOptions)
