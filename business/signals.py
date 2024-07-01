from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import business.models as biz_models

@receiver(post_save, sender=biz_models.BusinessProfile)
def create_profile_media(sender, instance, created, **kwargs):
    if created:
        biz_models.BusinessMedia.objects.create(business=instance)

@receiver(post_save, sender=biz_models.BusinessProfile)
def save_profile_media(sender, instance, **kwargs):
    instance.media.save()