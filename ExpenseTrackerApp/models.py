from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class transaction_details(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    amount = models.IntegerField()
    transaction_type = models.TextField()
    category = models.TextField()
    note = models.CharField(max_length= 500, null = True)

    def __str__(self):
        return str(self.user_id)
        
class categories(models.Model):
    type = models.TextField()
    name = models.CharField(max_length= 50)

    def __str__(self):
        return self.name



