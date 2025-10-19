from django.db import models

class Payment(models.Model):
    
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default='usd')
    status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "stripe_payment"
        managed = False

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"
    