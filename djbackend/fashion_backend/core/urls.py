from django.contrib import admin
from django.urls import path
from . import views

from core import views  # أو from your_app_name import views

urlpatterns = [
    
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/home/', views.HomeCategoryList.as_view(), name='home-category-list'),

    path('', views.ProductList.as_view(), name='product-list'),
    path('byType/', views.ProductListByClothesType.as_view(), name='list-by-type'),
    path('popular/', views.PopularProductsList.as_view(), name='popular-list'),
    path('search/', views.SearchProductByTitle.as_view(), name='search'),
    path('category/', views.FilterProductByCategory.as_view(), name='products-by-category'),  # مسار مُعدَّل: 'products/category/'
    path('recommendations/', views.SimilarProducts.as_view(), name='similar-products'),  # مسار مُعدَّل: 'products/recommendations/'
    # path('h/',views.Home.as_view(), name='home'),
    path('projects/',views.ProjectJSONView.as_view(), name='project-list'),
]