from django.db import models

class Department(models.Model):
    name=models.CharField(max_length=10,blank=False,null=False)
    meta=models.JSONField(default=dict)
    
    class Meta:
        db_table='department'
    
    def __str__(self):
        return self.name
    