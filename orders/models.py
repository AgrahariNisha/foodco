from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.TextField()
    total = models.FloatField()
    gst = models.FloatField()
    discount = models.FloatField()
    final_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username