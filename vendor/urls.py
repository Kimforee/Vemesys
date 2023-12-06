from django.urls import path
from .views import VendorListCreateView, VendorRetrieveUpdateDeleteView, \
    PurchaseOrderListCreateView, PurchaseOrderRetrieveUpdateDeleteView, \
    vendor_performance, acknowledge_purchase_order_view

urlpatterns = [
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(), name='purchase-order-retrieve-update-delete'),
    path('api/vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor-performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase_order_view, name='acknowledge-purchase-order'),
]
