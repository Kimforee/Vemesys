from django.db.models import Avg, Count
from django.utils import timezone
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.db.models import Avg, ExpressionWrapper, F, DurationField
from django.db.models.functions import Coalesce

def update_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(delivery_date__gt=timezone.now())
    total_completed_pos = completed_pos.count()
    on_time_deliveries = completed_pos.filter(delivery_date__lte=F('acknowledgment_date'))
    if total_completed_pos > 0:
        on_time_delivery_rate = (on_time_deliveries.count() / total_completed_pos) * 100
    else :
      vendor.on_time_delivery_rate = 0
    vendor.save()

def update_quality_rating_avg(vendor):
    completed_pos_with_ratings = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    quality_rating_avg = completed_pos_with_ratings.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
    if quality_rating_avg is not None:
        vendor.quality_rating_avg = quality_rating_avg
    else:
        quality_rating_avg = 0
    vendor.save()

from django.db.models import DurationField, ExpressionWrapper, F
from django.db.models.functions import Coalesce

def update_average_response_time(vendor):
    pos_with_acknowledgment = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    pos_with_acknowledgment = pos_with_acknowledgment.exclude(issue_date__isnull=True)
    pos_with_acknowledgment = pos_with_acknowledgment.filter(acknowledgment_date__gte=F('issue_date'))

    if pos_with_acknowledgment.exists():
        response_times = pos_with_acknowledgment.annotate(
            time_diff=ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=DurationField()
            )
        ).aggregate(avg_response_time=Avg('time_diff'))['avg_response_time']
        print(f"Response Times: {response_times}")
        print(f"Total Purchase Orders with Acknowledgment: {pos_with_acknowledgment.count()}")
        if response_times is not None:
            vendor.average_response_time = response_times.total_seconds() / pos_with_acknowledgment.count()
        else:
            vendor.average_response_time = 0
    else:
        vendor.average_response_time = 0
    vendor.save()


def update_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    successful_fulfillments = total_pos.filter(status='completed', acknowledgment_date__isnull=False)
    if total_pos.count() > 0:
      fulfillment_rate = (successful_fulfillments.count() / total_pos.count()) * 100 
    else :
        fulfillment_rate = 0
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
