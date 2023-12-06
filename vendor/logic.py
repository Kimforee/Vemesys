# logic.py

from django.db.models import Avg, Count
from django.utils import timezone
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.db.models import Avg, ExpressionWrapper, F, DurationField
from django.db.models.functions import Coalesce

def update_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(delivery_date__gt=timezone.now())
    total_completed_pos = completed_pos.count()
    on_time_deliveries = completed_pos.filter(delivery_date__lte=F('acknowledgment_date'))
    on_time_delivery_rate = (on_time_deliveries.count() / total_completed_pos) * 100 if total_completed_pos > 0 else 0
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()

def update_quality_rating_avg(vendor):
    completed_pos_with_ratings = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    quality_rating_avg = completed_pos_with_ratings.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
    vendor.quality_rating_avg = quality_rating_avg if quality_rating_avg is not None else 0
    vendor.save()

def update_average_response_time(vendor):
    # Filter purchase orders with acknowledgment
    pos_with_acknowledgment = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)

    # Calculate the average response time
    response_times = pos_with_acknowledgment.annotate(
        time_diff=ExpressionWrapper(
            Coalesce(F('acknowledgment_date') - F('issue_date'), 0),
            output_field=DurationField()
        )
    ).aggregate(avg_response_time=Avg('time_diff'))['avg_response_time']

    # Update the vendor's average_response_time field
    vendor.average_response_time = response_times.total_seconds() / pos_with_acknowledgment.count() if pos_with_acknowledgment.count() > 0 else 0
    vendor.save()

def update_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    successful_fulfillments = total_pos.filter(status='completed', issues__isnull=True)
    fulfillment_rate = (successful_fulfillments.count() / total_pos.count()) * 100 if total_pos.count() > 0 else 0
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

def update_vendor_performance_metrics(vendor):
    update_on_time_delivery_rate(vendor)
    update_quality_rating_avg(vendor)
    update_average_response_time(vendor)
    update_fulfillment_rate(vendor)

def acknowledge_purchase_order(po_id):
    purchase_order = PurchaseOrder.objects.get(pk=po_id)
    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()
    update_vendor_performance_metrics(purchase_order.vendor)
