from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Income, Expense, Category
from .forms import IncomeForm, ExpenseForm, CategoryForm
from .utils import (
    get_total_income, get_total_expenses, get_remaining_balance,
    get_expenses_by_category, get_current_month_year, get_monthly_summary,
)


@login_required
def dashboard(request):
    user = request.user
    month, year = get_current_month_year()
    context = {
        "total_income": get_total_income(user, month, year),
        "total_expenses": get_total_expenses(user, month, year),
        "balance": get_remaining_balance(user, month, year),
        "category_data": get_expenses_by_category(user, month, year),
        "recent_expenses": Expense.objects.filter(user=user).select_related("category")[:5],
        "month": month,
        "year": year,
    }
    return render(request, "expenses/dashboard.html", context)


@login_required
def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, f"Income of ${income.amount} added!")
            return redirect("dashboard")
    else:
        form = IncomeForm(initial={"date": timezone.now().date()})
    return render(request, "expenses/add_income.html", {"form": form})


@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == "POST":
        income.delete()
        messages.success(request, "Income entry deleted.")
    return redirect("expense_list")


@login_required
def add_expense(request):
    if not Category.objects.filter(user=request.user).exists():
        messages.warning(request, "Please create a category before adding an expense.")
        return redirect("manage_categories")
    if request.method == "POST":
        form = ExpenseForm(request.user, request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, f"Expense of ${expense.amount} recorded!")
            return redirect("expense_list")
    else:
        form = ExpenseForm(request.user, initial={"date": timezone.now().date()})
    return render(request, "expenses/add_expense.html", {"form": form})


@login_required
def expense_list(request):
    user = request.user
    today = timezone.now().date()
    try:
        month = int(request.GET.get("month", today.month))
        year = int(request.GET.get("year", today.year))
    except ValueError:
        month, year = today.month, today.year

    expenses = Expense.objects.filter(
        user=user, date__month=month, date__year=year
    ).select_related("category").order_by("-date")

    incomes = Income.objects.filter(
        user=user, date__month=month, date__year=year
    ).order_by("-date")

    context = {
        "expenses": expenses,
        "incomes": incomes,
        "total_income": get_total_income(user, month, year),
        "total_expenses": get_total_expenses(user, month, year),
        "balance": get_remaining_balance(user, month, year),
        "selected_month": month,
        "selected_year": year,
        "years": list(range(today.year - 2, today.year + 2)),
        "months": list(range(1, 13)),
    }
    return render(request, "expenses/expense_list.html", context)


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted.")
    return redirect("expense_list")


@login_required
def manage_categories(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if categories.filter(name__iexact=name).exists():
                messages.warning(request, f'Category "{name}" already exists.')
            else:
                cat = form.save(commit=False)
                cat.user = user
                cat.save()
                messages.success(request, f'Category "{cat.name}" created!')
                return redirect("manage_categories")
    else:
        form = CategoryForm()
    return render(request, "expenses/categories.html", {"form": form, "categories": categories})


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == "POST":
        category.delete()
        messages.success(request, f'Category "{category.name}" deleted.')
    return redirect("manage_categories")


@login_required
def report(request):
    today = timezone.now().date()
    try:
        year = int(request.GET.get("year", today.year))
    except ValueError:
        year = today.year
    context = {
        "monthly_summary": get_monthly_summary(request.user, year),
        "category_data": get_expenses_by_category(request.user),
        "selected_year": year,
        "years": list(range(today.year - 2, today.year + 1)),
    }
    return render(request, "expenses/report.html", context)
