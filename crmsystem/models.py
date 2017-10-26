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


class Employee(models.Model):
    # pracovnik musi spravovat aspon 1 znacku,
    # niejak rozumne to overit, napriklad pri jeho vytvarani 
    #titul, ci nechame jedno texto pole kde to proste napises,
    #alebo urobit moznost pridat titul, co ti stale rekurzivne 
    #prida do databazy field, alebo idealne iba prida na koniec 
    #stringu title
    #na datumy urobit taku peknu rozklikavacku kde is mozes vybrat a nemusis manualne pisat
    # po stlaceni cisel by ti malo niejak najst  danu hodnotu ak chceme nieco take implementovat 
    username = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    date_of_birth = models.DateField() 
    marks = models.ManyToManyField(Mark)

    def __str__(self):
        return (
            self.title + " " + self.name + " " + self.surname
        )

class Legal_person(models.Model):
    ico = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.ico

class Customer(models.Model):
    # TODO
    # Kontrola telefonneho cisla

    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    city = models.CharField(max_length=150)
    street_number = models.PositiveSmallIntegerField()
    street_name = models.CharField(max_length=150)
    telephone_number = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    legal_person = models.ForeignKey(Legal_person, on_delete=models.CASCADE)

    def __str__(self):
        return (
            self.email
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
        return self.name


class Contract(models.Model):
    # TODO
    # Aspon 1 oblecenie, kontrola cisla uctu

    # Tu nemoze byt pocet kusov, to sa vztahuje na oblecenie nie na zmluvu !!!!
    #number_of_pieces = models.IntegerField()

    total_cost = models.IntegerField()
    city = models.CharField(max_length=150)
    street_number = models.PositiveSmallIntegerField()
    street_name = models.CharField(max_length=150)
    account_iban_number = models.CharField(max_length=40)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.pk)


class Meeting(models.Model):
    description = models.TextField()
    customer = models.ManyToManyField(Customer)
    employee = models.ManyToManyField(Employee)

    def __str__(self):
        return str(self.pk) 


class Contain(models.Model):
    num_of_pieces = models.IntegerField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)