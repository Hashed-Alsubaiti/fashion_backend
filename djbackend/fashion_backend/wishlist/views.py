from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import serializers, models

class GetWishList(generics.ListAPIView):
    # pagination_class = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WishlistSerializer

    def get_queryset(self):
        print("self.request.user ",self.request.user)
        return models.WishList.objects.filter(userId = self.request.user)


class ToggleWishList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        product_id = request.query_params.get('id')

        if not user_id or not product_id:
            return Response({'message': 'Invalid Request: user id and product id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = models.Product.objects.get(id=product_id)
        except models.Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)  # تم تغيير حالة الرد إلى 404

        wishlist_item, created = models.WishList.objects.get_or_create(userId=request.user, product=product)

        if created:
            return Response({'message': 'Product added to wish list'}, status=status.HTTP_201_CREATED)
        else:
            wishlist_item.delete()
            return Response({'message': 'Product removed from wish list'}, status=status.HTTP_204_NO_CONTENT)


# Create your views here.
