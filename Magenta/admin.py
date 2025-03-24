from django.contrib import admin
from .models import Category, Template, SubCategory, TemplateImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class TemplateImageInline(admin.TabularInline):
    model = TemplateImage
    extra = 1 

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "created_at", "download_count")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TemplateImageInline]
    
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug')
    list_filter = ('category',)
    search_fields = ('title',)