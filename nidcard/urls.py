from django.contrib import admin
from django.urls import path
from .views import Home,PdfToText
urlpatterns = [
    path('', Home,name='home'),
    path('pdf', PdfToText,name='home'),
]
