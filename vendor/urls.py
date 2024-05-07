from django.urls import re_path as url
from vendor import views

urlpatterns = [
    url(r"^$", views.VendorAPIView.as_view()),
    url(r"^(?P<vendor_id>[a-zA-Z0-9-]+)/$", views.VendorAPIView.as_view()),
    url(r"^(?P<vendor_id>[a-zA-Z0-9-]+)/performance/$", views.VendorPerformanceAPIView.as_view()),
]