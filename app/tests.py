from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Category, PDFDocument


class PDFDocumentModelTests(TestCase):
    def test_title_is_generated_from_filename(self):
        category = Category.objects.create(name='Notes')
        document = PDFDocument.objects.create(
            category=category,
            pdf_file=SimpleUploadedFile('physics_notes.pdf', b'%PDF-1.4 test file', content_type='application/pdf'),
        )

        self.assertEqual(document.title, 'Physics Notes')
        self.assertTrue(document.slug.startswith('physics-notes'))


class PDFPreviewViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Handouts')
        self.document = PDFDocument.objects.create(
            category=self.category,
            pdf_file=SimpleUploadedFile('chemistry-guide.pdf', b'%PDF-1.4 test file', content_type='application/pdf'),
        )

    def test_list_page_contains_preview_trigger(self):
        response = self.client.get(reverse('pdf_list'))

        self.assertContains(response, 'Quick preview available')
        self.assertContains(response, 'preview-trigger')

    def test_detail_page_contains_embedded_preview(self):
        response = self.client.get(reverse('pdf_detail', kwargs={'slug': self.document.slug}))

        self.assertContains(response, 'Read before downloading')
        self.assertContains(response, 'application/pdf')
