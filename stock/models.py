from django.db import models
from django.utils.timezone import now


class Product(models.Model):
    name = models.CharField(max_length=100)  # Added max_length
    product_code = models.CharField(max_length=50, unique=True)  # Added max_length
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.name}'


class Customer(models.Model):
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50, default=' ')
    total_credit = models.FloatField(default=0.00)
    total_debit = models.FloatField(default=0.00)

    def __str__(self):
        return f'{self.name}'
    
    

class Bill(models.Model):
    bill_no = models.PositiveIntegerField(unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'Bill No: {self.bill_no}'


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    total = models.FloatField(default=0.00)

    def __str__(self):
        return f'Bill ID: {self.bill.id}'


class BillItemProduct(models.Model):
    bill_item = models.ForeignKey(BillItem, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.quantity * self.rate

    def __str__(self):
        return f"{self.product.name} (Qty: {self.quantity}, Rate: {self.rate}) for {self.bill_item.bill}"


class Credit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    date = models.DateField(default=now)
    particulars = models.CharField(max_length=255, editable=False, default=' ')  # Auto-filled field

    def save(self, *args, **kwargs):
        # Auto-update particulars with Bill number
        if not self.particulars:
            self.particulars = f"Bill No: {self.bill.bill_no}"
        super(Credit, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer} credited on {self.date}'


class Debit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    date = models.DateField(default=now)
    particulars = models.CharField(max_length=255, editable=False, default='Cheque')  # Auto-filled field

    def save(self, *args, **kwargs):
        # Auto-update particulars for Debit
        if not self.particulars:
            self.particulars = "Cheque"
        super(Debit, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer} Debited on {self.date}'
