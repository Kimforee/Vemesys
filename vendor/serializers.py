from rest_framework import serializers
from .models import Vendor, PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        # exclude = ['on_time_delivery_rate',
        #            'quality_rating_avg',
        #            'average_response_time',
        #            'fulfillment_rate']
        extra_kwargs = {
            'on_time_delivery_rate': {'required': False},
            'quality_rating_avg': {'required': False},
            'average_response_time': {'required': False},
            'fulfillment_rate': {'required': False},
        }

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'