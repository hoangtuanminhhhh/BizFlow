from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, unique=True, null=True)
    points = models.IntegerField(default=0) #Tích điểm

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def add_stock(self, amount):
        self.quantity += amount
        self.save()

    def deduct_stock(self, amount):
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=0)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)

    @property
    def get_cart_items(self):
        orderitem =  self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total

    @property
    def get_cart_total(self):
        orderitem =  self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])
        return total

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):   
        total = self.product.price * self.quantity
        return total
  
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=50, default="cash")
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.order.id}"
    

class StockTransaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_change = models.IntegerField()  # + vào khi nhập, - ra khi bán
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)