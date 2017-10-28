from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


TITLE_CHOICES = (
    ('Bc.', 'Bc.'),
    ('Ing.', 'Ing.'),
    ('Mgr.', 'Mgr.'),
    ('PhDr.', 'PhDr.'),
    ('PaedDr.', 'PaedDr.'),
    ('RNDr.', 'RNDr.'),
    ('MUDr.', 'MUDr.'),
    ('PhD.', 'PhD.')
)


class Mark(models.Model):
    designer_name = models.CharField(max_length=30)
    designer_surname = models.CharField(max_length=30)
    name_of_mark = models.CharField(max_length=30)
    #Get Pillow at https://pypi.python.org/pypi/Pillow or run command "pip install Pillow".
    #logo_of_mark = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)

    def __str__(self):
        return str(self.pk) + self.name_of_mark

    class Meta:
        permissions = (
            ("show_mark", "Can show mark"),
        )


class Employee(models.Model):
    username = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    date_of_birth = models.DateField() 
    marks = models.ManyToManyField(Mark)
    user_account = models.ForeignKey('auth.User')

    def __str__(self):
        return (
            self.title + " " + self.name + " " + self.surname
        )

    class Meta:
        permissions = (
            ("show_employee", "Can show employee info"),
        )


class Legal_person(models.Model):
    ico = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.ico


class Customer(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    city = models.CharField(max_length=150)
    street_number = models.PositiveSmallIntegerField()
    street_name = models.CharField(max_length=150)
    telephone_number = models.CharField(max_length=50)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )
    legal_person = models.ForeignKey(
        Legal_person,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return (
            self.email
        )

    class Meta:
        permissions = (
            ("edit_customer_info", "Can edit info without assignment"),
            ("assign_employee", "Can assign employee to customer"),
            ("show_customer", "Can show customer info"),
        )


class Cloth(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    color = models.IntegerField()
    size = models.PositiveSmallIntegerField()
    cost_of_piece = models.DecimalField(decimal_places=2, max_digits=12)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)
    #image_of_cloth = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=True)

    def getName(self):
        return self.name + " - " + str(self.size)

    def __str__(self):
        return str(self.pk) + " " + self.name

    class Meta:
        permissions = (
            ("show_cloth", "Can show cloth"),
        )


class Contract(models.Model):
    total_cost = models.IntegerField()
    city = models.CharField(max_length=150)
    street_number = models.PositiveSmallIntegerField()
    street_name = models.CharField(max_length=150)
    account_iban_number = models.CharField(max_length=40)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    class Meta:
        permissions = (
            ("show_contract", "Can show contract info"),
        )


class Meeting(models.Model):
    description = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk) 

    class Meta:
        permissions = (
            ("show_meeting", "Can show meeting info"),
        )


class Contain(models.Model):
    num_of_pieces = models.PositiveSmallIntegerField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)

    def __str__(self):
        return (
            str(self.contract.pk) + " " + self.cloth.name +
            " " + self.cloth.mark.name_of_mark +
            " - " + str(self.num_of_pieces)
        )
