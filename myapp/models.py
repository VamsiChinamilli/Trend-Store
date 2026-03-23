from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('dress', 'Dresses'),
        ('makeup', 'Makeup'),
        ('grocery', 'Groceries'),
        ('furniture', 'Furniture'),
        ('toys', 'Toys'),
    ]
    
    name = models.CharField(max_length=200)
    # Adding 'null=True' and 'blank=True' tells Django it's okay if this is empty for now
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image_url = models.URLField(max_length=500, null=True, blank=True) 

    def __str__(self):
        return self.name