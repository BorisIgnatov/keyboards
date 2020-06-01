from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Keyboard(models.Model):
    brand_name = models.ForeignKey('Brand',on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255)
    images = models.ManyToManyField('KeyboardImage')
    price = models.IntegerField()
    switches = models.ManyToManyField('Switch')
    description = models.TextField(null=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.brand_name.name + ' ' + self.model_name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='brands/images/',blank=True,)

    def __str__(self):
        return self.name


class Switch(models.Model):
    types = [
        ('lr','Linear'),
        ('cl','Clicky'),
        ('tl','Tactile'),
        ('df','No information')
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=2,choices=types,default='df')
    force = models.FloatField()
    image = models.ImageField(upload_to='switches/images/',null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    keyboard = models.ForeignKey('Keyboard',on_delete=models.CASCADE, null=True)
    images = models.ManyToManyField('ReviewImage',blank=True)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],)
    content = models.TextField()
    is_positive = models.BooleanField()


class ReviewImage(models.Model):
    image = models.ImageField(upload_to='review/images/')


class KeyboardImage(models.Model):
    image = models.ImageField(upload_to='keyboard/images/')
