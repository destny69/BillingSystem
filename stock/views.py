from django.shortcuts import render, get_object_or_404, HttpResponse,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bill, BillItem, BillItemProduct, Product, Customer, Credit, Debit
from django.utils.timezone import now
from weasyprint import HTML
from django.template.loader import render_to_string
from django.db.models import Q
from datetime import datetime
from django.db.models import Sum
from .forms import *
from django.contrib import messages


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
     # Get or create a Credit instance for the given customer
        customer = get_object_or_404(Customer, id=customer_id)
        credit, created = Credit.objects.get_or_create(bill=bill, customer=customer)

        # Update the credit amount and date
        credit.amount = bill_item.total
        credit.date = now().date()
        credit.save()

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




def generate_ledger(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    
    # Get all credit and debit transactions for the customer
    credits = Credit.objects.filter(customer=customer).order_by('date')
    debits = Debit.objects.filter(customer=customer).order_by('date')

    # Prepare a list of transactions to display
    transactions = []

    # Calculate the opening balance
    opening_balance = customer.total_credit - customer.total_debit  # or set a default value
    current_balance = opening_balance

    # Merge credits and debits into a single list of transactions
    for credit in credits:
        transactions.append({
            'date': credit.date,
            'particulars': f"Bill No. {credit.bill.bill_no}" if credit.bill else "Credit",
            'debit': 0.00,
            'credit': credit.amount,
            'balance': None  # Will calculate later
        })

    for debit in debits:
        transactions.append({
            'date': debit.date,
            'particulars': "Cheque" if debit.amount > 0 else "Debit",
            'debit': debit.amount,
            'credit': 0.00,
            'balance': None  # Will calculate later
        })

    # Sort transactions by date
    transactions.sort(key=lambda x: x['date'])

    # Update the balance for each transaction
    for transaction in transactions:
        if transaction['credit'] > 0:
            current_balance += transaction['credit']
        if transaction['debit'] > 0:
            current_balance -= transaction['debit']
        transaction['balance'] = current_balance

    # Date range filtering
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            transactions = [txn for txn in transactions if start_date <= txn['date'] <= end_date]
        except ValueError:
            # Handle invalid date input
            pass
    debit_form = DebitForm()
    return render(request, 'ledger_page.html', {
        'customer': customer,
        'transactions': transactions,
        'opening_balance': opening_balance,
        'start_date': start_date,
        'end_date': end_date,
        'debit_form':debit_form
    })



def debit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST":
        debit_form = DebitForm(request.POST)
        if debit_form.is_valid():
            debit_instance = debit_form.save(commit=False)
            debit_instance.customer = customer
            debit_instance.save()
            
            # Update customer total_debit
            customer.total_debit += debit_instance.amount
            customer.save()

            messages.success(request, "Debit added successfully.")
            return redirect("generate_ledger", customer_id=customer.id)


   
