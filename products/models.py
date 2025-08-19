from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    slug = models.SlugField(blank=True, null=True)
    NAME_CHOICES=[
        ('Feminine','Feminine'),
        ('Masculine','Masculine'),
        ('Childish','Childish'),
    ]
    name = models.CharField(max_length=50,choices=NAME_CHOICES)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



# Create your models here.
class Product(models.Model):
    slug = models.SlugField(blank=True, null=True)
    name=models.CharField(max_length=50)
    description=models.TextField(max_length=255)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    COLOR_CHOICE=[
        ('red','Red'),
        ('brown','Brown'),
        ('green','Green'),
        ('black','Black'),
        ('white','White'),
    ]
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    color=models.CharField(max_length=10,choices=COLOR_CHOICE)
    size=models.CharField(max_length=12,choices=SIZE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


   




