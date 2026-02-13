from django.db import models

class Department(models.Model):
    name=models.CharField(max_length=10,unique=True,blank=False,null=False)
    meta=models.JSONField(default=dict)
    active=models.BooleanField(default=True)
    
    class Meta:
        db_table='department'
    
    def __str__(self):
        return self.name
    