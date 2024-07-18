from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class UAV(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=6, decimal_places=2) 
    category = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uavs')


    def __str__(self):
        return f"{self.brand} {self.model} - {self.category}"

class RentalRecord(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    )
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE, related_name='rentals')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rentals')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.uav} rented by {self.user} from {self.start_date} to {self.end_date} - {self.status}"
    
    def check_date_conflict(self, start_date, end_date):
        return RentalRecord.objects.filter(
            uav=self.uav,
            status__in=['pending', 'active'],
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()
    


class UAVListing(models.Model):
    uav = models.OneToOneField(UAV, on_delete=models.CASCADE, related_name='listing')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Listing for {self.uav} - {'Listed' if self.is_listed else 'Unlisted'}"
