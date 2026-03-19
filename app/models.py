from pathlib import Path

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PDFDocument(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title or self.filename_stem

    @property
    def filename_stem(self):
        return Path(self.pdf_file.name).stem.replace('-', ' ').replace('_', ' ').title()

    @property
    def share_url(self):
        return reverse('pdf_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.pdf_file and not self.title:
            self.title = self.filename_stem
        if not self.slug:
            base_slug = slugify(self.title or self.filename_stem)
            slug = base_slug
            counter = 1
            while PDFDocument.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                counter += 1
                slug = f'{base_slug}-{counter}'
            self.slug = slug
        super().save(*args, **kwargs)
