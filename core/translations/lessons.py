from modeltranslation.translator import register, TranslationOptions
from core.models import Lesson


# Lesson translation
# ----------------------------------------------------------------------------------------------------------------------
# Lesson
@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title', 'about', )
