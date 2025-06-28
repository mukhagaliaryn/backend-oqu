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


# LessonDoc
class LessonDocs(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Lesson'), related_name="docs"
    )
    title = models.CharField(_('Title'), max_length=255)
    file = models.FileField(_('File'), upload_to='core/models/lessons/docs/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Lesson doc')
        verbose_name_plural = _('Lesson docs')


# Video
class Video(models.Model):
    TYPE_VIDEO_URL = (
        ('youtube', _('YouTube')),
        ('vimeo', _('Vimeo')),
    )

    lesson = models.OneToOneField(
        Lesson, on_delete=models.CASCADE,
        related_name='video', verbose_name=_('Lesson')
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


# Text
class Text(models.Model):
    lesson = models.OneToOneField(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Lesson'), related_name='text'
    )
    content = models.TextField(_('Content'))
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return _('Text: {}').format(self.lesson)

    class Meta:
        verbose_name = _('Text')
        verbose_name_plural = _('Texts')
        ordering = ('order', )


# Test model
# ----------------------------------------------------------------------------------------------------------------------
# Test
class Test(models.Model):
    lesson = models.OneToOneField(
        Lesson, on_delete=models.CASCADE,
        related_name='test', verbose_name=_('Lesson')
    )
    title = models.CharField(_('Title'), max_length=128)
    description = models.TextField(_('Description'), blank=True, null=True)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return _('Test: {}').format(self.lesson)

    class Meta:
        verbose_name = _('Test')
        verbose_name_plural = _('Tests')
        ordering = ('order', )


# Question
class Question(models.Model):
    QUESTION_TYPE = (
        ('simple', _('Simple answer')),
        ('multiple', _('Multiple answer')),
    )

    test = models.ForeignKey(
        Test, on_delete=models.CASCADE,
        related_name='questions', verbose_name=_('Test')
    )
    text = models.TextField(_('Question text'))
    question_type = models.CharField(_('Question type'), max_length=64, choices=QUESTION_TYPE, default='simple')
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return _('Question: ID{}').format(self.pk)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ('order', )


# Answer
class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE,
        related_name='answers', verbose_name=_('Question')
    )
    text = models.TextField(_('Answer text'))
    is_correct = models.BooleanField(_('Is correct'), default=False)

    def __str__(self):
        return _('Answer: ID{}').format(self.pk)

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        