from performance.models import HistoricalPerformance
from purchase.models import PurchaseOrder
from django.db import models
from datetime import datetime


def update_vendor_performance(vendor):
    """
    Update the HistoricalPerformance for the given vendor.
    """
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).exclude(status='canceled')
    on_time_delivery_rate = (completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date')).count() / total_orders.count()) * 100 if total_orders.count() != 0 else 0
    quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False).aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating'] or 0
    average_response_time = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).aggregate(avg_response=models.Avg(models.F('acknowledgment_date') - models.F('issue_date')))['avg_response'].total_seconds() / 3600 if PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).exists() else 0
    fulfillment_rate = (completed_orders.count() / total_orders.count()) * 100 if total_orders.count() != 0 else 0

    historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor, date=datetime.now())
    historical_performance.on_time_delivery_rate = on_time_delivery_rate
    historical_performance.quality_rating_avg = quality_rating_avg
    historical_performance.average_response_time = average_response_time
    historical_performance.fulfillment_rate = fulfillment_rate
    historical_performance.save()