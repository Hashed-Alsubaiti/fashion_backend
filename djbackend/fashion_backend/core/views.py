from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics,status
from . import models, serializers  # أو from your_app_name import models, serializers
from django.db.models import Count
import random
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

class HomeCategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        # الحصول على جميع الفئات
        queryset = models.Category.objects.all()

        
        #-----------------------------------------------------------------
        # استخدام order_by للحصول على ترتيب عشوائي (أكثر كفاءة من shuffle)
        # queryset = queryset.order_by('?')  # علامة الاستفهام (?) تعني ترتيب عشوائي

        # return queryset[:5]  # إرجاع أول 5 عناصر
        #---------------------------------------------------
        queryset = queryset.annotate(random_order=Count('id')) 
        queryset=list(queryset)
        random.shuffle(queryset)
        return queryset[:5]

class BrandList(generics.ListAPIView):
    serializer_class = serializers.BrandSerializer
    queryset = models.Brand.objects.all()

class ProductList(generics.ListAPIView):
    # permission_classes = [AllowAny]  # السماح للجميع بالوصول
    serializer_class = serializers.ProductSerializer
        #-----------------------------------------------------------------
    # استخدام order_by للحصول على ترتيب عشوائي (أكثر كفاءة من shuffle)
    # queryset = queryset.order_by('?')  # علامة الاستفهام (?) تعني ترتيب عشوائي
    # print('++++++++',queryset)
    # return queryset[:5] 
    def get_queryset(self):
    #     print('get_queryset ')
        # return 0
        # الحصول على جميع الفئات
        queryset = models.Product.objects.all()
         #-----------------------------------------------------------------
        # استخدام order_by للحصول على ترتيب عشوائي (أكثر كفاءة من shuffle)
        queryset = queryset.order_by('?')  # علامة الاستفهام (?) تعني ترتيب عشوائي
        # print('++++++++',queryset)
        return queryset[:5]  # إرجاع أول 5 عناصر
        #---------------------------------------------------
        # queryset = queryset.annotate(random_order=Count('id')) 
        # queryset=list(queryset)
        # random.shuffle(queryset)
        # return queryset[:20]

class PopularProductsList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self,request):
        # الحصول على المنتجات ذات التقييم بين 4 و 5
        queryset = models.Product.objects.filter(rating__gte=4.0, rating__lte=5.0)

        # ترتيب عشوائي باستخدام order_by (أكثر كفاءة)
        queryset = queryset.order_by('?')

        return queryset[:20]  # إرجاع أول 20 عنصر

class ProductListByClothesType(APIView):
    # permission_classes = [AllowAny]
    serializer_class = serializers.ProductSerializer
    

    def get(self, request):
        clothes_type = request.query_params.get('clothesType', None)

        if clothes_type:
            print("clothes_type ",clothes_type)
            queryset = models.Product.objects.filter(clothesType=clothes_type)

            # ترتيب عشوائي باستخدام order_by (أكثر كفاءة)
            random_queryset = queryset.order_by('?') 

            limited_products = random_queryset[:20]

            serializer = serializers.ProductSerializer(limited_products, many= True)

            return Response(serializer.data)  # إرجاع أول 20 عنصر
        else:
            # إذا لم يتم تحديد clothesType، يمكنك إرجاع جميع المنتجات أو queryset فارغ
            return Response({'message': ' no query products'}, status= status.HTTP_400_BAD_REQUEST)  # أو return models.Product.objects.all()
    
    

class SimilarProducts(APIView):
    def get(self, request):
        category = request.query_params.get('category', None)
        

        if category:
            products = models.Product.objects.filter(category=category)

            if products.exists():  # التحقق من وجود منتجات قبل التلاعب بها
                product_list = list(products)
                random.shuffle(product_list)
                limited_products = product_list[:6]
                serializer = serializers.ProductSerializer(limited_products, many=True)
                return Response(serializer.data)
            else:
                return Response({'message': 'No products found for this category'}, status=status.HTTP_404_NOT_FOUND)  # تحسين حالة الرد

        else:
            return Response({'message': 'No category provided'}, status=status.HTTP_400_BAD_REQUEST)
        


class SearchProductByTitle(APIView):
    def get(self, request):
        query = request.query_params.get('q', None)

        if query:
            products = models.Product.objects.filter(title_icontains=query)  # استخدام __icontains للبحث الحساس لحالة الأحرف

            if products.exists():  # التحقق من وجود منتجات قبل التسلسل
                serializer = serializers.ProductSerializer(products, many=True)
                return Response(serializer.data)
            else:
                return Response({'message': 'No products found for this query'}, status=status.HTTP_404_NOT_FOUND)  # تحسين حالة الرد

        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        

class FilterProductByCategory(APIView):
    # permission_classes = [AllowAny]
    print("////////////////////////")
    def get(self, request):
        print("****************")
        category = request.query_params.get('category', None)  # استخدام get للحصول على قيمة parameter
        print('category ',category)
        if category:
            print('category ',category)
            products = models.Product.objects.filter(category=category)

            if products.exists():  # التحقق من وجود منتجات قبل التسلسل
                serializer = serializers.ProductSerializer(products, many=True)
                return Response(serializer.data)
            else:
                return Response({'message': 'No products found for this category'}, status=status.HTTP_404_NOT_FOUND)  # تحسين حالة الرد

        else:
            return Response({'message': 'No category provided'}, status=status.HTTP_400_BAD_REQUEST)
        

from .models import Product
from .serializers import ProductSerializer
class ProjectJSONView(APIView):
    permission_classes = [AllowAny]  # السماح للجميع بالوصول
    def get(self, request, *args, **kwargs):
        projects = Product.objects.all()
        serializer = ProductSerializer(projects, many=True)
        return Response(serializer.data)
