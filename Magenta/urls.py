from django.urls import path, include
from .views import CategoryViewSet, TemplateViewSet, SubCategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'templates', TemplateViewSet, basename='template')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')

urlpatterns = [
    path('', include(router.urls)),
]
