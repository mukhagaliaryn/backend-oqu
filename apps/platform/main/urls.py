from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainAPIView.as_view()),
    path('blog/', views.BlogAPIView.as_view()),
    path('blog/<pk>/', views.BlogDetailAPIView.as_view()),
]
