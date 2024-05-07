from django.urls import re_path as url
from purchase import views

urlpatterns = [
    url(r"^$", views.PurchaseOrderAPIView.as_view()),
    url(r"^(?P<po_id>[a-zA-Z0-9-]+)/$", views.PurchaseOrderAPIView.as_view()),
    url(r"^(?P<po_id>[a-zA-Z0-9-]+)/acknowledge/", views.PurchaseOrderAcknowledgeAPIView.as_view(), name='acknowledge-purchase-order'),
]