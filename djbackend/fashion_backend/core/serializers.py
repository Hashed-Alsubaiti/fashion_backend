from rest_framework import serializers
from . import models  # أو from your_app_name import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'title', 'imageUrl')  # تحديد الحقول التي سيتم تضمينها في ال JSON

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ('id', 'title', 'imageUrl')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'  # استخدام __all__ لتضمين جميع الحقول أو تحديد ['field1', 'field2', ...] بشكل يدوي