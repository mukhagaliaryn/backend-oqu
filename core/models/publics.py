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
    content = models.TextField(_('Content'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
        ordering = ('-created_at', )
