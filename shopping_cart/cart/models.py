from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField()

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            # Default image URL 
            return '/static/default-image.jpg'  

    def __str__(self):
        return self.name
    


class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.amount * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

