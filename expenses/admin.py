from django.contrib import admin
from .models import Category, Income, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "source", "date")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "amount", "description", "date")
