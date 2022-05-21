from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from order.models import OrderDetail
from product.models import Product, Category
from product.serializers import ProductSerializer,CategorySerializer
from utils.paginator import StandardResultsSetPagination


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        category=request.GET.get('category',None)
        queryset=self.get_queryset()
        if category:
            queryset=queryset.filter(category=category)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartViewSet(ModelViewSet):
    queryset = OrderDetail.objects.all()
    permission_classes = [IsAuthenticated,]
    def list(self, request, *args, **kwargs):
        user=request.user
        order_detail=OrderDetail.objects.filter(order__customer=user)
        return Response({'items':[
            {
                'item_id':item.id,
                'order_id':item.order.id,
                'product':item.product.name,
                'image':item.product.imageURL(),
                'quantity':item.quantity,
                'price':item.total_price()
            }
            for item in order_detail
        ]})