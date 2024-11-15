from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import Text
from bot.texts import manager


@receiver(pre_save, sender=Text)
def remove_old_title_on_title_change(sender, instance, **kwargs):
    """Remove the old title from Redis if the title changes."""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if old_instance.title != instance.title:
                manager.delete_text(old_instance)
        except ObjectDoesNotExist:
            pass


@receiver(post_save, sender=Text)
def update_redis_on_save(sender, instance, **kwargs):
    """Update Redis when a Text object is saved."""
    manager.update_text(instance)


@receiver(post_delete, sender=Text)
def update_redis_on_delete(sender, instance, **kwargs):
    """Delete text from Redis when a Text object is deleted."""
    manager.delete_text(instance)
