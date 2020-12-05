from django.db import models
from django.db.models import CASCADE


class PurchaseModel(models.Model):
    purchaser_name = models.CharField(max_length=50)
    quantity = models.IntegerField()

    def __str__(self):
        return self.purchaser_name

class PurchaseStatusModel(models.Model):
    purchase = models.ForeignKey(PurchaseModel, on_delete=CASCADE)
    status = models.CharField(max_length=25,
    choices= (
        ('open', 'Open'),
        ('verified', 'Verified'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
        )
              )

    created_at = models.DateTimeField(db_index=True)
    def __str__(self):
        return str(self.purchase)