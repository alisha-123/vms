import uuid

from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

from vendor.models import Vendor

class HistoricalPerformance(TimeStampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()