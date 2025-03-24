from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="category_images", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Template(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='templates')
    file = models.FileField(upload_to="template_files", blank=True, null=True)
    video = models.FileField(upload_to="template_videos", blank=True, null=True)  # Добавляем поле для видео
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    download_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"

class TemplateImage(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="template_images")

    def __str__(self):
        return f"Image for {self.template.title}"


class SubCategory(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    image = models.ImageField(upload_to="sub_category_images", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"subcategory {self.title}"
    
    