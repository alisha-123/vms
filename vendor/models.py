import uuid

from django.db import models
from model_utils.models import TimeStampedModel

class Vendor(TimeStampedModel):
    vendor_code = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    contact_details = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)


