from django.db.models.signals import post_save
from django.dispatch import receiver
from vendor.models import Vendor
from performance.utils import update_vendor_performance


@receiver(post_save, sender=Vendor)
def update_historical_performance_on_vendor_change(sender, instance, created, **kwargs):
    """
    Signal handler to update HistoricalPerformance when a Vendor is saved or updated.
    """
    update_vendor_performance(instance)


