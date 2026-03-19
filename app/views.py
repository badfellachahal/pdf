from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, PDFDocument


def pdf_list(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    documents = PDFDocument.objects.select_related('category').all()
    if query:
        documents = documents.filter(
            Q(title__icontains=query)
            | Q(category__name__icontains=query)
            | Q(pdf_file__icontains=query)
        )

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        documents = documents.filter(category=active_category)

    context = {
        'documents': documents,
        'categories': Category.objects.all(),
        'query': query,
        'active_category': active_category,
        'total_documents': documents.count(),
    }
    return render(request, 'app/pdf_list.html', context)


def pdf_detail(request, slug):
    document = get_object_or_404(PDFDocument.objects.select_related('category'), slug=slug)
    related_documents = PDFDocument.objects.filter(category=document.category).exclude(pk=document.pk)[:4]
    return render(
        request,
        'app/pdf_detail.html',
        {
            'document': document,
            'related_documents': related_documents,
        },
    )
