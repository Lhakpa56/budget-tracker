from django.db.models import Sum
from django.utils import timezone
from .models import Income, Expense


def get_total_income(user, month=None, year=None):
    qs = Income.objects.filter(user=user)
    if month and year:
        qs = qs.filter(date__month=month, date__year=year)
    return qs.aggregate(total=Sum("amount"))["total"] or 0


def get_total_expenses(user, month=None, year=None):
    qs = Expense.objects.filter(user=user)
    if month and year:
        qs = qs.filter(date__month=month, date__year=year)
    return qs.aggregate(total=Sum("amount"))["total"] or 0


def get_remaining_balance(user, month=None, year=None):
    return get_total_income(user, month, year) - get_total_expenses(user, month, year)


def get_expenses_by_category(user, month=None, year=None):
    qs = Expense.objects.filter(user=user)
    if month and year:
        qs = qs.filter(date__month=month, date__year=year)
    return list(qs.values("category__name").annotate(total=Sum("amount")).order_by("-total"))


def get_current_month_year():
    today = timezone.now().date()
    return today.month, today.year


def get_monthly_summary(user, year):
    import calendar
    summary = []
    for month in range(1, 13):
        income = get_total_income(user, month=month, year=year)
        expenses = get_total_expenses(user, month=month, year=year)
        summary.append({
            "month": month,
            "month_name": calendar.month_abbr[month],
            "income": float(income),
            "expenses": float(expenses),
            "balance": float(income - expenses),
        })
    return summary
