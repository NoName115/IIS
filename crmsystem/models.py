from django.db import models
from django.utils import timezone


class Customer(models.Model):
    city = models.CharField(max_length=150)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=150)
    email = models.EmailField()
    telephone_number = models.CharField(max_length=50)
    some_date = models.DateTimeField(
        blank=True, null=True
    )

    class Meta:
        permissions = (
            ("set_date", "Can set date"),
        )

    def setDate(self):
        self.some_date = timezone.now()
        self.save()

    def __str__(self):
        return self.email
