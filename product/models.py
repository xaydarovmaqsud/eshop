from django.db import models
from django_currentuser.middleware import get_current_user,get_current_authenticated_user

class Category(models.Model):
    name=models.CharField(max_length=150)
    description=models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='products')
    name=models.CharField(max_length=150)
    price=models.FloatField()
    image=models.ImageField(null=True,blank=True)
    quantity=models.IntegerField(default=0)

    def get_status(self):
        if self.quantity>0:
            cuser=get_current_authenticated_user()
            if cuser:
                if cuser.orders.all():
                    order=get_current_authenticated_user().orders.order_by('-id').first()
                    for item in order.details.all():
                        if self == item.product:
                            return 'Added to cart'
                    return 'Add to cart'
                else:
                    return 'Add to cart'
            else:
                return 'Add to cart'
        else:
            return 'Unavailable'

    def imageURL(self):
        if self.image:
            return self.image.url
        return ''
    def __str__(self):
        return self.name