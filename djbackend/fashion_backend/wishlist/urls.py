from django.urls import path

from . import views  # أو from your_app_name import views

urlpatterns = [
    path('toggle/', views.ToggleWishList.as_view(), name='add-remove-from-wishlist'),
    path('me/', views.GetWishList.as_view(), name='get-wishlist'),
]