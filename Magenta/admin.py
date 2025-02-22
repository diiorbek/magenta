from django.contrib import admin
from .models import Category, Template

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')