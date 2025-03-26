from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.courses import Course, Chapter


# Lesson model
# ----------------------------------------------------------------------------------------------------------------------
# Lesson
class Lesson(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='lessons', verbose_name=_('Course')
    )
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE,
        related_name='lessons', verbose_name=_('Chapter')
    )
    about = models.TextField(_('About'), blank=True, null=True)
    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    last_update = models.DateTimeField(_('Last update'), auto_now=True)
    duration = models.PositiveSmallIntegerField(_('Duration (min)'), default=0)
    access = models.BooleanField(_('Access'), default=True)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
        ordering = ('order', )


# Video
class Video(models.Model):
    TYPE_VIDEO_URL = (
        ('youtube', _('YouTube')),
        ('vimeo', _('Vimeo')),
    )

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        related_name='videos', verbose_name=_('Lesson')
    )
    url_type = models.CharField(_('URL type'), max_length=64, choices=TYPE_VIDEO_URL, default='youtube')
    url = models.CharField(_('URL'), max_length=255)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return _('Video: {}').format(self.lesson)

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
        ordering = ('order', )
