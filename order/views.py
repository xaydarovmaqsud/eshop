from django.http import JsonResponse
from django.shortcuts import render
import json

# Create your views here.
from order.models import Order, OrderDetail
from product.models import Product
from utils.decarators import is_verified
from utils.utils import get_order_count


def add_cart(request):
    event=''
    pid=None
    if request.method == 'POST':
        data:dict=json.loads(request.body)
        product=Product.objects.get(id=data['product_id'])
        user_orders=request.user.orders.all().order_by('-id')
        pid=product.id
        if user_orders:
            order=user_orders.first()
        else:
            order=Order.objects.create(
                customer=request.user
            )
        if product.quantity>0:
            order_detail=OrderDetail.objects.filter(
                order=order,
                product=product
            ).first()
            if order_detail:
                order_detail.delete()
                event='deleted'
            else:
                order_detail=OrderDetail.objects.create(
                    order=order,
                    product=product
                )
                event='added'
    return JsonResponse({
        'items_count':order.item_coun(),
        'event':event,
        'pid':pid
    })

@is_verified
def orders_cart(request):
    order=request.user.orders.last()
    return render(
        request=request,
        template_name='orders/orders_cart.html',
        context={
            'order':order,
            'badge_count':get_order_count(request)

        }
    )

def change_quantity(request):
    item=None
    if request.method == 'POST':
        data:dict=json.loads(request.body)
        item_id=data.get('item',None)
        action=data.get('action',None)
        value=data.get('value',None)
        if item_id and action:
            item=OrderDetail.objects.get(id=item_id)
            item.change_quantity(action,value)
    response={
        'error':False,
        'item_quantity':item.quantity,
        'item':item.id,
        'total_price':item.total_price(),
        'total':item.order.total_price()
    }if item else{
        'error':True
    }
    return JsonResponse(response)

def item_remove(request,id):
    try:
        item=OrderDetail.objects.get(id=id)
        order=item.order
        item.delete()
        success=True
    except:
        success=False
        order=None
    return JsonResponse({
        'success':success,
        'total':order.total_price() if order else 0,
        'id':id,
        'items_count':order.details.count()
    })