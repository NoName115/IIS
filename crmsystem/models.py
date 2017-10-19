from django.db import models
from django.utils import timezone


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
    # pridatvat znacky bude vediet iba majitel a zamestannec
    # v ER je ze kazda znacka by mala mat aspon 1 typ oblecenia,
    # bude niejake tlacidlo na znacky co ti ich zobrazi, a tie co
    # nebudu mat ziadne typy oblecenia budu bud sive bez hyperlinku,
    # alebo zobrazi stranku ze : zial momentlalne nemame na sklade 
    # zbozi danej znacky alebo nieco na ten styl 
    designer_name = models.CharField(max_length=30)
    designer_surname = models.CharField(max_length=30)
    name_of_mark = models.CharField(max_length=30)
    # zatial neotestovane ale chcelo nieco instalovat,
    #Get Pillow at https://pypi.python.org/pypi/Pillow or run command "pip install Pillow".
    #logo_of_mark = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)

    def __str__(self):
        return self.name_of_mark


class Employee(models.Model):
    # pracovnik musi spravovat aspon 1 znacku,
    # niejak rozumne to overit, napriklad pri jeho vytvarani 
    #titul, ci nechame jedno texto pole kde to proste napises,
    #alebo urobit moznost pridat titul, co ti stale rekurzivne 
    #prida do databazy field, alebo idealne iba prida na koniec 
    #stringu title
    #na datumy urobit taku peknu rozklikavacku kde is mozes vybrat a nemusis manualne pisat
    # po stlaceni cisel by ti malo niejak najst  danu hodnotu ak chceme nieco take implementovat 
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    date_of_birth = models.DateField() 
    marks = models.ManyToManyField(Mark)

    def __str__(self):
        return (self.name + self.surname)

class Customer(models.Model):
    #rozumnu kontrolu formatu cisla tel.
    #dal by som tam natvrdo predponu +421 a skontroloval pocet cisel
    customer_id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=150)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=150)
    email = models.EmailField()
    telephone_number = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return ("id zakaznika: " + str(self.customer_id) + " "  + self.email)

class Cloth(models.Model):
    # dobrovolna moznost pridania obrazku, 
    # nech nemusime stahovat jak blazni pri plneni databazy
    name = models.CharField(max_length=50)
    description = models.TextField()
    color = models.IntegerField()
    size = models.IntegerField()
    cost_of_piece = models.FloatField()
    #image_of_cloth = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=True)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Contract(models.Model):
    #kontrola ci  obsahuje aspon niejake oblecenie(taka samozrejmost)
    #vypocet celkovej sumy
    #kontrola cisla uctu, nekomplikovat, 
    # asi len IBAN podporovat a spocitat znaky tym padom
    contract_id = models.IntegerField(primary_key=True)
    number_of_pieces = models.IntegerField()
    total_cost = models.IntegerField()
    city = models.CharField(max_length=150)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=150)
    account_iban_number = models.IntegerField() 
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    clothes = models.ManyToManyField(Cloth)

    def __str__(self):
        return str(self.contract_id)


class Meeting(models.Model):
    meeting_id = models.IntegerField(primary_key=True)
    some_date = models.DateTimeField( blank=True, null=True)
    description = models.TextField()
    customer = models.OneToOneField(Customer)
    employee = models.OneToOneField(Employee)
 
    def setDate(self):
        self.some_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.meeting_id) 
class Physical_person(models.Model):
    physical_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    customer = models.OneToOneField(Customer)

    def __str__(self):
        return (self.name + self.surname +"id FO: " + str(self.physical_id)) 

class Legal_person(models.Model):
    name = models.CharField(max_length=50)
    ico = models.CharField(primary_key=True, max_length=50)
    customer = models.OneToOneField(Customer)
    physical_person = models.ForeignKey(Physical_person, on_delete=models.CASCADE)

    def __str__(self):
        return (self.ico)


    



    
