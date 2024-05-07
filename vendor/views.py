from __future__ import annotations

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vendor.models import Vendor
from vendor.serializers import VendorPerformanceSerializer
from vendor.serializers import VendorSerializer


class VendorAPIView(GenericAPIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id=None):
        queryset = Vendor.objects.all()
        try:
            if vendor_id:
                queryset = Vendor.objects.get(vendor_code=vendor_id)
                serializer = VendorSerializer(queryset)
                return Response(
                    {
                        'details': serializer.data,

                    },
                    status=status.HTTP_200_OK,
                )
            queryset = Vendor.objects.all()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = VendorSerializer(queryset, many=True)
            return Response(
                {
                    'details': serializer.data,

                },
                status=status.HTTP_200_OK,
            )
        except Vendor.DoesNotExist:
            return Response(
                {'details': 'Vendor object does not exist.'}, status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(e)
            return Response(
                {'details': 'Some Error Occurred.'}, status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        try:
            serializer = VendorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {'details': serializer.errors}, status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:

            return Response(
                {'details': 'Some Error Occurred.'}, status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, vendor_id=None):
        try:
            queryset = Vendor.objects.get(vendor_code=vendor_id)
            serializer = VendorSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {'details': serializer.errors}, status.HTTP_400_BAD_REQUEST,
            )
        except Vendor.DoesNotExist:
            return Response(
                {'details': 'Vendor object does not exist.'}, status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:

            return Response(
                {'details': 'Some Error Occurred.'}, status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, vendor_id=None):
        try:
            queryset = Vendor.objects.get(vendor_code=vendor_id)
            queryset.delete()
            return Response({'details': 'Successfully deleted'}, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response(
                {'details': 'Vendor object does not exist.'}, status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:

            return Response(
                {'details': 'Some Error Occurred.'}, status=status.HTTP_400_BAD_REQUEST,
            )


class VendorPerformanceAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id=None):
        queryset = Vendor.objects.all()
        try:

            queryset = Vendor.objects.get(vendor_code=vendor_id)
            serializer = VendorPerformanceSerializer(queryset)
            return Response(
                {
                    'details': serializer.data,

                },
                status=status.HTTP_200_OK,
            )
        except Vendor.DoesNotExist:
            return Response(
                {'details': 'Vendor object does not exist.'}, status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {'details': 'Some Error Occurred.'}, status=status.HTTP_400_BAD_REQUEST,
            )
