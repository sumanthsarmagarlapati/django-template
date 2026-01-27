from decimal import Decimal
from django.db import models
from .department_model import Department
from .address_model import Address
from .tags_model import Tags

class Employee(models.Model):
    id=models.BigAutoField(primary_key=True,db_column='id',editable=False)
    name=models.CharField(unique=True,max_length=20,blank=False)
    email=models.EmailField(unique=True,blank=True)
    salary=models.DecimalField(max_digits=15,null=False,decimal_places=2,default=Decimal('0.00'))
    department=models.ForeignKey(Department,on_delete=models.PROTECT,null=False,related_name='employee')
    address=models.OneToOneField(Address,on_delete=models.SET_NULL,null=True,related_name='employee')
    tags=models.ManyToManyField(Tags,related_name='employees',through='EmployeeTags')
    active=models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name}-{self.email}-{self.department}"
    
    class Meta:
        db_table='employee'
        indexes=[
            models.Index(fields=["name"],name="idx_employee_name"),
            models.Index(fields=["department"],name="idx_employee_department"),
            models.Index(fields=["address"],name="idx_employee_address"),
            models.Index(fields=["active"],name="idx_employee_active")
        ]
    
    
class EmployeeTags(models.Model):
    id=models.BigAutoField(primary_key=True,db_column='id',editable=False)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,null=False)
    tag=models.ForeignKey(Tags,on_delete=models.CASCADE,null=False)
    active=models.BooleanField(default=True)
    
    def __str__(self):
        return f"Employee tag {self.employee}-{self.tag} -{self.active}"
    
    class Meta:
        db_table='employee_tag'
        indexes=[models.Index(fields=["employee","tag"],name="idx_employee_tag")]
    
    
    
    
    