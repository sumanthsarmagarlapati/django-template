from django.db import models

class Tags(models.Model):
    name=models.CharField(max_length=20,null=False,blank=False)
    
    class Meta:
        db_table="tags"
    
    def __str__(self):
        return f"{self.name}"
        