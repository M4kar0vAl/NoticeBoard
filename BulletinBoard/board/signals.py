from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Response, Advert
from .tasks import response_created_notify, advert_created_notify


@receiver(post_save, sender=Response)
def new_response(instance, created, **kwargs):
    """
    If new Response instance is created, send email to author of advertisement.
    """
    if created:
        response_created_notify.delay(pk=instance.pk)


@receiver(post_save, sender=Advert)
def new_advert(instance, created, **kwargs):
    """
    If a new advert is created, then notify all users subscribed to advert category
    """
    if created:
        advert_created_notify.delay(pk=instance.pk)
