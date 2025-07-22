from django.db import models
import uuid

class Order(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    order_number = models.CharField(max_length=15,unique=True, editable=False,blank=True, null=True)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    shipping_address = models.TextField()
    product_name = models.CharField(max_length=255)
    wood_type = models.CharField(max_length=100)
    size = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='In Progress')

    created_at = models.DateTimeField(auto_now_add=True)
    stripe_session_id = models.CharField(max_length=255)


    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            if last_order and last_order.order_number:
                last_number = int(last_order.order_number.split('-')[1])
            else:
                last_number = 0
            new_number = last_number + 1
            self.order_number = f"MQ-{new_number:03d}"  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.customer_name} - {self.product_name} ({self.wood_type}, {self.size}) x{self.quantity}"
