from django.db import models
from django.utils.translation import gettext_lazy as _


# Blog models
# ----------------------------------------------------------------------------------------------------------------------
# Category
class BlogCategory(models.Model):
    name = models.CharField(_('Blog category'), max_length=128)
    slug = models.SlugField(_('Key'), unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Blog category')
        verbose_name_plural = _('Blog categories')


# Blog
class Blog(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.CASCADE,
        related_name='blogs', verbose_name=_('Blog category')
    )
    shortcut = models.TextField(_('Shortcut'), max_length=300, blank=True, null=True)
    content = models.TextField(_('Content'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
        ordering = ('-created_at', )


# FAQ
# ----------------------------------------------------------------------------------------------------------------------
class FAQ(models.Model):
    title = models.CharField(_('Title'), max_length=128)
    content = models.TextField(_('Content'))
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('FAQ')
        ordering = ('order', )
