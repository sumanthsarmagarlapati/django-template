from django.db import models

class Address(models.Model):
    line1 = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    
    class Meta:
        db_table = 'address'
    
    def __str__(self):
        return f"{self.line1}, {self.city}"