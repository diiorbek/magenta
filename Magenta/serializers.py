from rest_framework import serializers
from .models import Category, Template, SubCategory, TemplateImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['slug']  
        

class TemplateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateImage
        fields = ['id', 'image']
        
class TemplateSerializer(serializers.ModelSerializer):
    images = TemplateImageSerializer(many=True, read_only=True)  # Чтение связанных изображений
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )  # Для загрузки новых изображений

    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])  # Достаем изображения
        template = Template.objects.create(**validated_data)  # Создаем шаблон

        for image in uploaded_images:
            TemplateImage.objects.create(template=template, image=image)  # Добавляем изображения

        return template

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])  # Достаем новые изображения
        instance = super().update(instance, validated_data)  # Обновляем шаблон

        for image in uploaded_images:
            TemplateImage.objects.create(template=instance, image=image)  # Добавляем изображения

        return instance

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        read_only_fields = ['slug']

