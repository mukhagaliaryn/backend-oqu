from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User


# Category
# ----------------------------------------------------------------------------------------------------------------------
# Category
class Category(models.Model):
    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(_('Key'), max_length=128)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('order', )


# Subcategory
class Subcategory(models.Model):
    own = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='sub_categories', verbose_name=_('Category')
    )
    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(_('Key'), max_length=128)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')
        ordering = ('order', )


# Course
# ----------------------------------------------------------------------------------------------------------------------
# Language
class Language(models.Model):
    name = models.CharField(_('Name'), max_length=64)
    slug = models.SlugField(_('Key'), max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')


# Course
class Course(models.Model):
    name = models.CharField(_('Name'), max_length=128)
    category = models.ForeignKey(
        Category, related_name='courses',
        on_delete=models.CASCADE, verbose_name=_('Category')
    )
    sub_category = models.ForeignKey(
        Subcategory, related_name='sub_courses',
        on_delete=models.CASCADE, verbose_name=_('Subcategory')
    )
    poster = models.ImageField(_('Poster'), upload_to='core/models/courses/', blank=True, null=True)
    about = models.TextField(_('About'), blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    languages = models.ManyToManyField(Language, related_name='courses', verbose_name=_('Languages'), blank=True)
    authors = models.ManyToManyField(
        User, verbose_name=_('Authors'),
        related_name="courses", blank=True
    )
    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    last_update = models.DateField(_('Last update'), auto_now=True)
    rating = models.DecimalField(_('Rating'), max_digits=2, decimal_places=1, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ('-date_created', )


# Chapter
class Chapter(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='chapters', verbose_name=_('Course')
    )
    name = models.CharField(_('Name'), max_length=128)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')
        ordering = ('order', )
