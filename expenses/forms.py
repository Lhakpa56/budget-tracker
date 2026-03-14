from django import forms
from .models import Income, Expense, Category


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["amount", "source", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "amount": forms.NumberInput(attrs={"placeholder": "0.00", "step": "0.01", "min": "0.01"}),
            "source": forms.TextInput(attrs={"placeholder": "e.g. Part-time job, Allowance"}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["category", "amount", "description", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "amount": forms.NumberInput(attrs={"placeholder": "0.00", "step": "0.01", "min": "0.01"}),
            "description": forms.TextInput(attrs={"placeholder": "What did you spend on?"}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(user=user)
        self.fields["category"].empty_label = "-- Select category --"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Food, Transport, Rent"}),
        }
