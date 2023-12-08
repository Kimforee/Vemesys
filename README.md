# Vendor Management System
 Vendor Management System with Performance Metrics

Introduction
Welcome to the Vendor Management System (VMS) with Performance Metrics, a Django-based web application designed to streamline vendor-related operations and provide insightful performance metrics. This system serves as a comprehensive solution for managing vendor profiles, tracking purchase orders, and evaluating vendor performance.

# Installation Steps
1. Clone the repository: `git clone https://github.com/Kimforee/Vemesys.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Apply migrations: `python manage.py migrate`

# Test Execution
python manage.py test

Vendor Profile Management
`Create a new vendor
POST /api/vendors/: Create a new vendor profile.

List all vendors
GET /api/vendors/: Retrieve a list of all vendors.

Retrieve a specific vendor's details
GET /api/vendors/{vendor_id}/: Retrieve details of a specific vendor.

Update a vendor's details
PUT /api/vendors/{vendor_id}/: Update details of a specific vendor.

Delete a vendor
DELETE /api/vendors/{vendor_id}/: Delete a specific vendor.

Purchase Order Tracking

Create a purchase order
POST /api/purchase_orders/: Create a new purchase order.

List all purchase orders
GET /api/purchase_orders/: Retrieve a list of all purchase orders.

Retrieve details of a specific purchase order
GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order. 

Update a purchase order
PUT /api/purchase_orders/{po_id}/: Update details of a specific purchase order.

Delete a purchase order
DELETE /api/purchase_orders/{po_id}/: Delete a specific purchase order.

Vendor Performance Evaluation
Retrieve a vendor's performance metrics
GET /api/vendors/{vendor_id}/performance/: Retrieve calculated performance metrics for a specific vendor.

Acknowledge a purchase order
POST /api/purchase_orders/{po_id}/acknowledge/: Acknowledge a purchase order.

Data Models
Vendor Model
Fields: name, contact_details, address, vendor_code, on_time_delivery_rate, quality_rating_avg, average_response_time, fulfillment_rate.

Purchase Order (PO) Model
Fields: po_number, vendor, order_date, delivery_date, items, quantity, status, quality_rating, issue_date, acknowledgment_date.

Historical Performance Model
Fields: vendor, date, on_time_delivery_rate, quality_rating_avg, average_response_time, fulfillment_rate.


