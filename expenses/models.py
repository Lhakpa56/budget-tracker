from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]
        unique_together = ("name", "user")

    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incomes")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=150, blank=True, default="")
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} - ${self.amount} on {self.date}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="expenses"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, default="")
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.category})"
