from django import forms
from django.forms import inlineformset_factory
from .models import Bill, BillItem, BillItemProduct, Debit

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['bill_no', 'customer', 'date']

class BillItemProductForm(forms.ModelForm):
    class Meta:
        model = BillItemProduct
        fields = ['product', 'quantity', 'rate']

# Inline formset to handle multiple BillItemProducts for a single BillItem
BillItemProductFormSet = inlineformset_factory(
    BillItem, 
    BillItemProduct, 
    form=BillItemProductForm,
    extra=1,  # Number of empty forms to display
    can_delete=True  # Allow deletion of items
)


class DebitForm(forms.ModelForm):
    class Meta:
        model = Debit
        fields = ['amount', 'date']
        