from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User, Course, Lesson, Chapter


# UserCourse
# ----------------------------------------------------------------------------------------------------------------------
class UserCourse(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_courses', verbose_name=_('User')
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='user_courses', verbose_name=_('Course')
    )
    is_completed = models.BooleanField(_('Is completed'), default=False)

    def __str__(self):
        return '{}: {}'.format(self.course.name, self.user)

    class Meta:
        verbose_name = _('User course')
        verbose_name_plural = _('User courses')


# UserChapter
# ----------------------------------------------------------------------------------------------------------------------
class UserChapter(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_chapters', verbose_name=_('User')
    )
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE,
        related_name='user_chapters', verbose_name=_('Chapter')
    )
    user_course = models.ForeignKey(
        UserCourse, on_delete=models.CASCADE,
        related_name='user_chapters', verbose_name=_('User course')
    )
    is_completed = models.BooleanField(_('Is completed'), default=False)

    def __str__(self):
        return '{}: {}'.format(self.chapter, self.user)

    class Meta:
        verbose_name = _('User chapter')
        verbose_name_plural = _('User chapters')


# UserLesson
# ----------------------------------------------------------------------------------------------------------------------
class UserLesson(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_lessons', verbose_name=_('User')
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        related_name='user_lessons', verbose_name=_('Lesson')
    )
    user_course = models.ForeignKey(
        UserCourse, on_delete=models.CASCADE,
        related_name='user_lessons', verbose_name=_('User course')
    )
    is_completed = models.BooleanField(_('Is completed'), default=False)

    def __str__(self):
        return '{}: {}'.format(self.lesson, self.user)

    class Meta:
        verbose_name = _('User lesson')
        verbose_name_plural = _('User lessons')
        ordering = ('lesson__order', )
