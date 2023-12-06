from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework import generics, status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .logic import acknowledge_purchase_order, update_vendor_performance_metrics

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

@api_view(['GET'])
def vendor_performance(request, vendor_id):
    vendor = Vendor.objects.get(pk=vendor_id)
    update_vendor_performance_metrics(vendor)
    serializer = VendorSerializer(vendor)
    return Response(serializer.data)
    # return Response({
    # "on_time_delivery_rate": serializer.data["on_time_delivery_rate"],
    # "quality_rating_avg": serializer.data["quality_rating_avg"],
    # "average_response_time": serializer.data["average_response_time"],
    # "fulfillment_rate": serializer.data["fulfillment_rate"]
# })

@api_view(['POST'])
def acknowledge_purchase_order_view(request, po_id):
    acknowledge_purchase_order(po_id)
    return Response({"message": "Purchase order acknowledged successfully."}, status=status.HTTP_200_OK)

