from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User, Course, Lesson, Chapter, Answer, Video, Text, Test, Question


# UserCourse
# ----------------------------------------------------------------------------------------------------------------------
class UserCourse(models.Model):
    COURSE_STATUS = (
        ('no-started', _('No started')),
        ('in-progress', _('In progress')),
        ('finished', _('Finished')),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_courses', verbose_name=_('User')
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='user_courses', verbose_name=_('Course')
    )
    score = models.DecimalField(_('Score (%)'), max_digits=5, decimal_places=2, default=0)
    status = models.CharField(_('Status'), choices=COURSE_STATUS, max_length=64, default='no-started')
    is_completed = models.BooleanField(_('Is completed'), default=False)

    def __str__(self):
        return _('Course: {} - User: {}').format(self.course.name, self.user)

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
    score = models.DecimalField(_('Score (%)'), max_digits=5, decimal_places=2, default=0)
    is_completed = models.BooleanField(_('Is completed'), default=False)

    def __str__(self):
        return _('Chapter: {} - User: {}').format(self.chapter, self.user)

    class Meta:
        verbose_name = _('User chapter')
        verbose_name_plural = _('User chapters')


# UserLesson
# ----------------------------------------------------------------------------------------------------------------------
# UserLesson
class UserLesson(models.Model):
    LESSON_STATUS = (
        ('no-started', _('No started')),
        ('in-progress', _('In progress')),
        ('finished', _('Finished')),
    )

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
    score = models.DecimalField(_('Score (%)'), max_digits=5, decimal_places=2, default=0)
    status = models.CharField(_('Status'), choices=LESSON_STATUS, max_length=64, default='no-started')
    is_completed = models.BooleanField(_('Is completed'), default=False)

    def __str__(self):
        return _('Lesson: {} - User: {}').format(self.lesson, self.user)

    class Meta:
        verbose_name = _('User lesson')
        verbose_name_plural = _('User lessons')
        ordering = ('lesson__order', )


# UserVideo
class UserVideo(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_videos', verbose_name=_('User')
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE,
        related_name='user_video', verbose_name=_('Video')
    )
    user_lesson = models.ForeignKey(
        UserLesson, on_delete=models.CASCADE,
        related_name='user_video', verbose_name=_('User lesson')
    )
    score = models.DecimalField(_('Score (%)'), max_digits=5, decimal_places=2, default=0)
    is_completed = models.BooleanField(_('Is completed'), default=False)

    def __str__(self):
        return _('Video: {} - User: {}').format(self.video, self.user)

    class Meta:
        verbose_name = _('User video')
        verbose_name_plural = _('User videos')
        ordering = ('video__order', )


# UserText
class UserText(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_texts', verbose_name=_('User')
    )
    text = models.ForeignKey(
        Text, on_delete=models.CASCADE,
        related_name='user_text', verbose_name=_('Text')
    )
    user_lesson = models.ForeignKey(
        UserLesson, on_delete=models.CASCADE,
        related_name='user_text', verbose_name=_('User lesson')
    )
    score = models.DecimalField(_('Score (%)'), max_digits=5, decimal_places=2, default=0)
    is_completed = models.BooleanField(_('Is completed'), default=False)

    def __str__(self):
        return _('Text: {} - User: {}').format(self.text, self.user)

    class Meta:
        verbose_name = _('User text')
        verbose_name_plural = _('User texts')
        ordering = ('text__order', )


# UserTest
class UserTest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_tests', verbose_name=_('User')
    )
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE,
        related_name='user_test', verbose_name=_('Test')
    )
    user_lesson = models.ForeignKey(
        UserLesson, on_delete=models.CASCADE,
        related_name='user_test', verbose_name=_('User lesson')
    )
    score = models.DecimalField(_('Score (%)'), max_digits=5, decimal_places=2, default=0)
    is_completed = models.BooleanField(_('Is completed'), default=False)
    submitted_at = models.DateTimeField(_('Submitted at'), auto_now_add=True)

    def __str__(self):
        return _('Test: {} - User: {}').format(self.test, self.user)

    class Meta:
        verbose_name = _("User test")
        verbose_name_plural = _("User tests")
        ordering = ('test__order', )


# UserAnswer
class UserAnswer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_answers', verbose_name=_('User'),
    )
    user_test = models.ForeignKey(
        UserTest, on_delete=models.CASCADE,
        related_name='user_answers', verbose_name=_('Test'), null=True, blank=True
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE,
        related_name='user_answers', verbose_name=_('Question'), null=True, blank=True
    )
    selected_answers = models.ManyToManyField(Answer, related_name='user_answers', verbose_name=_('Selected answers'))
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _('User answer: ID{} - User: {}').format(self.pk, self.user)

    class Meta:
        verbose_name = _('User answer')
        verbose_name_plural = _('User answers')
