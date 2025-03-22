from django.db.models.signals import post_save
from django.dispatch import receiver

from smartkassa.models import ClientService


@receiver(post_save, sender=ClientService)
def charge_client_for_service(sender, instance: ClientService, created, **kwargs):
    if created:
        client = instance.client
        client.balance = client.balance - instance.price_at_usage
        client.save(update_fields=["balance"])
