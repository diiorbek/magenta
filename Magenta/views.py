from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils.text import slugify
from .models import Category, Template
from .serializers import CategorySerializer, TemplateSerializer



class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    Manage template categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        """Automatically generates slug if not provided."""
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.name)
            instance.save()

    def destroy(self, request, *args, **kwargs):
        """Customize delete response message."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Category deleted successfully!"})

    @action(detail=False, methods=['get'], url_path='all')
    def all_categories(self, request):
        """Retrieve all categories."""
        categories = Category.objects.all()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)



class TemplateViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    Manage templates.
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        """Automatically generates slug if not provided."""
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.name)
            instance.save()

    def destroy(self, request, *args, **kwargs):
        """Customize delete response message."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Template deleted successfully!"})

    @action(detail=False, methods=['get'], url_path='all')
    def all_templates(self, request):
        """Retrieve all templates."""
        templates = Template.objects.all()
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)