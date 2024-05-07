from purchase.models import PurchaseOrder
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from purchase.constants import Status
from django.db import models
from performance.utils import update_vendor_performance

@receiver(post_save, sender=PurchaseOrder)
def update_purchase_order_related(sender, instance, created, **kwargs):
    completed_pos = PurchaseOrder.objects.filter(vendor=instance.vendor, status=Status.COMPLETED)
    if instance.status == 'completed':
        on_time_deliveries = completed_pos.filter(delivery_date__lte=instance.delivery_date).count()
        instance.vendor.on_time_delivery_rate = on_time_deliveries / completed_pos.count() if completed_pos.count() != 0 else 0

        completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        quality_rating_avg = completed_pos_with_rating.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
        instance.vendor.quality_rating_avg = quality_rating_avg

    if instance.acknowledgment_date:
        response_time = instance.acknowledgment_date - instance.issue_date
        instance.vendor.average_response_time = PurchaseOrder.objects.filter(vendor=instance.vendor).aggregate(models.Avg(response_time))['response_time__avg']

    total_pos = PurchaseOrder.objects.filter(vendor=instance.vendor).count()
    fulfillment_rate = completed_pos / total_pos if total_pos!=0 else 0
    instance.vendor.fulfillment_rate = fulfillment_rate
    instance.vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_historical_performance_on_purchase_order_change(sender, instance, created, **kwargs):
    """
    Signal handler to update HistoricalPerformance when a PurchaseOrder is saved or updated.
    """
    if created or instance.status == 'completed' or instance.status == 'canceled':
        update_vendor_performance(instance.vendor)

@receiver(post_delete, sender=PurchaseOrder)
def update_historical_performance_on_purchase_order_delete(sender, instance, **kwargs):
    """
    Signal handler to update HistoricalPerformance when a PurchaseOrder is deleted.
    """
    update_vendor_performance(instance.vendor)