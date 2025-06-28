from django.urls import path
from .views import get_subcategories


urlpatterns = [
    path('get_subcategories/', get_subcategories, name='get_subcategories'),
]