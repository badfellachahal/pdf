from django.contrib import admin

from .models import Category, PDFDocument


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at')
    list_filter = ('category', 'uploaded_at')
    search_fields = ('title', 'category__name', 'pdf_file')
    readonly_fields = ('uploaded_at', 'updated_at')
    autocomplete_fields = ('category',)

    def save_model(self, request, obj, form, change):
        if obj.pdf_file and not obj.title:
            obj.title = obj.filename_stem
        super().save_model(request, obj, form, change)
