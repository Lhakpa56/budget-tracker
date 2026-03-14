from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("income/add/", views.add_income, name="add_income"),
    path("income/delete/<int:pk>/", views.delete_income, name="delete_income"),
    path("expenses/add/", views.add_expense, name="add_expense"),
    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/delete/<int:pk>/", views.delete_expense, name="delete_expense"),
    path("categories/", views.manage_categories, name="manage_categories"),
    path("categories/delete/<int:pk>/", views.delete_category, name="delete_category"),
    path("report/", views.report, name="report"),
]
