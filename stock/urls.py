from django.urls import path
from . import views

urlpatterns = [
    path('bills/create/', views.create_bill, name='create_bill'),
    path('bills/add-item/', views.add_bill_item_ajax, name='add_bill_item_ajax'),
    path('bills/pdf/<int:bill_id>/', views.generate_bill_pdf, name='generate_bill_pdf'),
    # path('customer/<int:customer_id>/transactions/history', views.transaction_history, name='transaction_history'),
    path('customer/<int:customer_id>/transactions/', views.generate_ledger, name='generate_ledger'),
    path('debit/<int:customer_id>/', views.debit, name="debit"),

  ] 

