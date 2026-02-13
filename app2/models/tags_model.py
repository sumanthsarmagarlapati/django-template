from django.db import models


class Tags(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="id", editable=False)
    name = models.CharField(max_length=20, null=False, blank=False)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return f"{self.id}-{self.name}-{self.active}"
