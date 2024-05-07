from datetime import timedelta
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from purchase.models import PurchaseOrder
from purchase.serializers import PurchaseOrderSerializer

class PurchaseOrderAPIView(GenericAPIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, po_id=None):
        try:
            if po_id:
                queryset = PurchaseOrder.objects.get(po_number=po_id)
                serializer = PurchaseOrderSerializer(queryset)
                return Response(
                    {
                        "details": serializer.data,
                        
                    },
                    status=status.HTTP_200_OK,
                )
            queryset = PurchaseOrder.objects.all()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = PurchaseOrderSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = PurchaseOrderSerializer(queryset, many=True)
            return Response(
                {
                    "details": serializer.data,
                    
                },
                status=status.HTTP_200_OK,
            )
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"details": "Purchase Order object does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"details": "Some Error Occurred."}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:
            serializer = PurchaseOrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"details": serializer.errors}, status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            
            return Response(
                {"details": "Some Error Occurred."}, status=status.HTTP_400_BAD_REQUEST
            )
        
    def put(self, request, po_id=None):
        try:
            queryset = PurchaseOrder.objects.get(po_number=po_id)
            serializer = PurchaseOrderSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"details": serializer.errors}, status.HTTP_400_BAD_REQUEST
            )
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"details": "Purchase Order object does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            
            return Response(
                {"details": "Some Error Occurred."}, status=status.HTTP_400_BAD_REQUEST
            )
        
    def delete(self, request, po_id=None):
        try:
            queryset = PurchaseOrder.objects.get(po_number=po_id)
            queryset.delete()
            return Response({"details": "Successfully deleted"}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"details": "Purchase Order object does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            
            return Response(
                {"details": "Some Error Occurred."}, status=status.HTTP_400_BAD_REQUEST
            )
        
class PurchaseOrderAcknowledgeAPIView(GenericAPIView):
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_purchase_order(self, po_id):
        return PurchaseOrder.objects.get(po_number=po_id)

    def post(self, request, po_id):
        try:
            instance = self.get_purchase_order(po_id)
            if instance.acknowledgment_date:
                return Response({"message": "This purchase order has already been acknowledged."}, status=status.HTTP_400_BAD_REQUEST)

            instance.acknowledgment_date = timezone.now()
            instance.save()

            vendor = instance.vendor
            response_times = [po.acknowledgment_date - po.issue_date for po in vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False)]
            if response_times:
                vendor.average_response_time = sum(response_times, timedelta()) / len(response_times)
                vendor.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"details": "Purchase Order object does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            
            return Response(
                {"details": "Some Error Occurred."}, status=status.HTTP_400_BAD_REQUEST
            )