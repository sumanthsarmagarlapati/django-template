from django.db import models


class Address(models.Model):
    id = models.BigAutoField(
        primary_key=True, null=False, editable=False, db_column="id"
    )
    line = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    active=models.BooleanField(default=True)

    class Meta:
        db_table = "address"

    def __str__(self):
        return f"{self.id}-{self.line}, {self.city}"
