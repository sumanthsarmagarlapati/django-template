from django.db.models.signals import post_save
from django.dispatch import receiver
from app1.models.department_model import Department


@receiver(post_save, sender=Department)
def user_created(sender, instance, created, **kwargs):
    if created:
        print(f"Department created successfully: {instance.name}")
