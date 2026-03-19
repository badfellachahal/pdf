from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

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
