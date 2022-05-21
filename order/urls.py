from django.urls.conf import path
from .views import add_cart,orders_cart,change_quantity,item_remove

urlpatterns=[
    path('add-cart/',add_cart,name='add_cart'),
    path('items/',orders_cart,name='orders_cart'),
    path('change-quantity/',change_quantity,name='change-quantity'),
    path('remove/<int:id>/',item_remove,name='item_remove')
]