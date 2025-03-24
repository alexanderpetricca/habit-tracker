from django.db.models.signals import post_delete
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from .models import CustomUser


@receiver(post_delete, sender=CustomUser)
def delete_email_addresses(sender, instance, **kwargs):
    EmailAddress.objects.filter(user=instance).delete()
