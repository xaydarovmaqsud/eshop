from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class Customer(AbstractUser):
    GENDER_CHOISE=(
        ('MALE','male'),
        ('FEMALE', 'female')
    )
    phone_number=models.CharField(
        max_length=150,
        unique=True
    )
    username=models.CharField(
        max_length=150,
        unique=True,
        null=True
    )
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    middle_name = models.CharField(max_length=255,null=True,blank=True)
    gender = models.CharField(max_length=10,null=True,choices=GENDER_CHOISE,default='')
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True,null=True,blank=True)
    is_verified=models.BooleanField(default=False)
    image=models.ImageField(null=True,blank=True)

    @classmethod
    def create_user(cls, phone_number, password=None, **extra_fields):
        user: cls=cls.objects.filter(phone_number=phone_number)
        if user:
            return 'This phone number is busy!'
        else:
            user = Customer.objects.create(
                phone_number=phone_number,
                password=password
            )
            user.set_password(password)
            user.save()
        return user

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username','email']

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.phone_number


class Verification(models.Model):
    code = models.IntegerField(unique=True)
    user = models.ForeignKey(Customer,on_delete=models.CASCADE)

    @classmethod
    def code_generate(cls,user):
        new_code=random.randint(10000,100000)
        while cls.objects.filter(code=new_code):
            new_code=random.randint(10000,100000)
        obj=cls.objects.create(
            code=new_code,
            user=user
        )
        return obj