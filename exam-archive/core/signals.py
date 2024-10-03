from django.db.models.signals import post_delete
from django.dispatch import receiver

from core.models import Exam


@receiver(post_delete, sender=Exam)
def auto_delete_exam_file_on_delete(sender, instance: Exam, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
