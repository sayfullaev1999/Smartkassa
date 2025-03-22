from django.db.models.signals import post_save
from django.dispatch import receiver

from smartkassa.models import ClientService, BalanceTransaction


@receiver(post_save, sender=ClientService)
def charge_client_for_service(sender, instance: ClientService, created, **kwargs):
    """Списывает стоимость услуги с баланса клиента при создании записи об использовании услуги."""
    if created:
        BalanceTransaction.objects.create(
            client=instance.client,
            amount=-instance.price_at_usage,
            comment=f"Списание за услугу: {instance.service.name}"
        )


@receiver(post_save, sender=BalanceTransaction)
def update_client_balance_after_transaction(sender, instance: BalanceTransaction, created, **kwargs):
    """Обновляет баланс клиента при создании новой транзакции."""
    if created:
        client = instance.client
        client.balance += instance.amount
        client.save(update_fields=["balance"])
