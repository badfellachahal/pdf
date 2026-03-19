from django.urls import path

from . import views

urlpatterns = [
    path('', views.pdf_list, name='pdf_list'),
    path('pdf/<slug:slug>/', views.pdf_detail, name='pdf_detail'),
]
