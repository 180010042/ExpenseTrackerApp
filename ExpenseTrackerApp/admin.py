from django.contrib import admin
from ExpenseTrackerApp.models import transaction_details, categories

# Register your models here.
admin.site.register(transaction_details)
admin.site.register(categories)
