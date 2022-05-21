from rest_framework.routers import DefaultRouter
from product.api_views import ProductViewset,CategoryViewset,CartViewSet
router=DefaultRouter()

router.register('product',ProductViewset,basename='product'),
router.register('category',CategoryViewset,basename='category')
router.register('cart',CartViewSet,basename='cart')