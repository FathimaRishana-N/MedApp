from django.db import models

# Create your models here.


class login(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=20)
class pharmacy(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.BigIntegerField()
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    LOGIN = models.ForeignKey(login,default=1,on_delete=models.CASCADE)
class Medicine(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200,default='Liquid')
class user(models.Model):
    name = models.CharField(max_length=200)
    phone = models.BigIntegerField()
    Housename=models.CharField(max_length=200)
    place=models.CharField(max_length=200)
    post=models.CharField(max_length=200)
    pin = models.BigIntegerField()
    email = models.CharField(max_length=20)
    LOGIN = models.ForeignKey(login, default=1, on_delete=models.CASCADE)
class Feedback(models.Model):
    feedback = models.CharField(max_length=200)
    USER = models.ForeignKey(user, default=1, on_delete=models.CASCADE)
    date = models.CharField(max_length=200)
class Rating(models.Model):
    userrating = models.CharField(max_length=200)
    review = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    USER = models.ForeignKey(user, default=1, on_delete=models.CASCADE)
    PHARMACY = models.ForeignKey(pharmacy, default=1, on_delete=models.CASCADE)

class stock(models.Model):
    MEDICINE = models.ForeignKey(Medicine, default=1, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)
    file = models.CharField(max_length=200, default=1)
    size = models.CharField(max_length=200, default=1)
    price = models.CharField(max_length=200, default=1)
    PHARMACY = models.ForeignKey(pharmacy, default=1, on_delete=models.CASCADE)



class cart(models.Model):
    USER = models.ForeignKey(user, default=1, on_delete=models.CASCADE)
    PHARMACY = models.ForeignKey(pharmacy, default=1, on_delete=models.CASCADE)
    STOCK = models.ForeignKey(stock, default=1, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)

class purchase(models.Model):
    date = models.CharField(max_length=200)
    purchase = models.CharField(max_length=200)
    status = models.CharField(max_length=200,default='pending')
    Delievery = models.CharField(max_length=200)
    USER = models.ForeignKey(user, default=1, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    PHARMACY = models.ForeignKey(pharmacy, on_delete=models.CASCADE)


class purchasehub(models.Model):
    STOCK = models.ForeignKey(stock, default=1, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)
    PURCHASE = models.ForeignKey(purchase, default=1, on_delete=models.CASCADE)








