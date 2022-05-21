from django.db import models
from account.models import Customer
from product.models import Product

class Order(models.Model):
    STATUSES=[
        ('PENDING','pending'),
        ('INPROGRESS', 'inprogress'),
        ('COMPLATED', 'complated'),
        ('CANCELED', 'canceled')
    ]
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name='orders')
    order_date=models.DateTimeField(auto_now_add=True)
    required_date=models.DateTimeField(null=True)
    shipped_date=models.DateTimeField(null=True)
    canceled_date=models.DateTimeField(null=True)
    status=models.CharField(max_length=10,choices=STATUSES,default='PENDING')

    def __str__(self):
        return f'{self.customer.__str__()} - order:{self.id}'
    def item_coun(self):
        return self.details.count()

    def total_price(self):
        return sum([i.total_price() for i in self.details.all()])

class OrderDetail(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='details')
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name='orders')
    quantity=models.IntegerField(default=1)

    def total_price(self):
        return self.product.price*self.quantity

    def change_quantity(self,action,value=None):
        if action == 'plus':
            if self.quantity+1 <= self.product.quantity:
                self.quantity += 1
        elif action == 'minus':
            if self.quantity-1 >= 1:
                self.quantity -= 1
        elif value:
            value=int(value)
            if value>self.product.quantity:
                value=self.product.quantity
            elif value<1:
                value=1
            self.quantity=value
        self.save()

    def __str__(self):
        return f'order{self.order.id} - {self.product}, quantity:{self.quantity} shaxs:{self.order.customer}'