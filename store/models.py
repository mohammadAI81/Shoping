from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255)

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # image = models.ImageField(upload_to='/cover/product/')
    slug = models.SlugField(blank=True, null=True)
    inventory = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.BooleanField(default=True)
    width = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='product')
    color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name='product')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='product')
    discount = models.BooleanField(default=False, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    RATING_CHOICES = [
        ('1', 'Very Bad'),
        ('2', 'Bad'),
        ('3', 'Normal'),
        ('4', 'Good'),
        ('5', 'Very Good'),
    ]

    email = models.EmailField()
    published = models.BooleanField()
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, blank=True)
    body = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name}: {self.body[:16]}'


class Like(models.Model):
    person = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.person.username} -> {self.product.name}'
