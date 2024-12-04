from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bill, BillItem, BillItemProduct, Product, Customer
from django.utils.timezone import now
from weasyprint import HTML
from django.template.loader import render_to_string


def create_bill(request):
    products = Product.objects.all()
    customers = Customer.objects.all()
    return render(request, 'create_bill.html', {'products': products, 'customers': customers})


@csrf_exempt
def add_bill_item_ajax(request):
    if request.method == 'POST':
        bill_id = request.POST.get('bill_id', None)
        bill_no = request.POST.get('bill_no')
        customer_id = request.POST.get('customer_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        rate = float(request.POST.get('rate', 0.0))

        # Ensure customer_id and product_id are provided
        if not customer_id or not product_id:
            return JsonResponse({'error': 'Customer and product must be provided.'}, status=400)

        # Create or get the bill
        if not bill_id:  # If bill_id is not provided, create a new bill
            bill = Bill.objects.create(
                bill_no=bill_no,
                customer_id=customer_id,
                date=now().date(),
            )
        else:  # Retrieve existing bill
            bill = get_object_or_404(Bill, id=bill_id, )

        # Create or get the BillItem for this bill
        bill_item, created = BillItem.objects.get_or_create(bill=bill)

        # Add a new BillItemProduct
        product = get_object_or_404(Product, id=product_id)
        bill_item_product = BillItemProduct.objects.create(
            bill_item=bill_item,
            product=product,
            quantity=quantity,
            rate=rate # Ensure rate is Decimal
        )

        # Update BillItem total
        bill_item.total += bill_item_product.get_subtotal() # Convert subtotal to Decimal
        bill_item.save()

        return JsonResponse({
            'bill_id': bill.id,
            'product_name': product.name,
            'quantity': bill_item_product.quantity,
            'rate': bill_item_product.rate,
            'subtotal': bill_item_product.get_subtotal(),
            'total': bill_item.total,
        })

    return JsonResponse({'error': 'Invalid method'}, status=400)





def generate_bill_pdf(request, bill_id):
    # Fetch the bill and related data
    bill = Bill.objects.get(id=bill_id)
    bill_items = bill.billitem_set.prefetch_related('products')

    # Context for the template
    context = {
        'bill': bill,
        'bill_items': bill_items,
        'total': sum(item.total for item in bill_items),
    }

    # Render the template to HTML
    html_string = render_to_string('bill_pdf_template.html', context)

    # Generate PDF from HTML
    pdf_file = HTML(string=html_string).write_pdf()

    # Create a response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Bill_{bill.bill_no}.pdf"'

    return response