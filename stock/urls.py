from django.urls import path
from . import views

urlpatterns = [
    path('bills/create/', views.create_bill, name='create_bill'),
    path('bills/add-item/', views.add_bill_item_ajax, name='add_bill_item_ajax'),
    path('bills/pdf/<int:bill_id>/', views.generate_bill_pdf, name='generate_bill_pdf'),
]

