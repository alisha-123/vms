import uuid

from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

from vendor.models import Vendor
from purchase.constants import Status

class PurchaseOrder(TimeStampedModel):
    po_number = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_purchase')
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=Status.as_choices, default=Status.PENDING)
    quality_rating = models.FloatField(null=True, blank=True, default=0.0)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
