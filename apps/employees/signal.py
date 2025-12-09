from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Employee

User = get_user_model()

@receiver(post_save, sender=Employee)
def create_user_for_employee(sender, instance, created, **kwargs):
    if created and not instance.user:
        # Puedes usar el DNI o número de documento como username
        username = instance.document_number
        email = instance.email or f"{username}@example.com"
        password = User.objects.make_random_password()

        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        instance.user = user
        instance.save()
