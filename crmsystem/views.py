from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *


def default_web(request):
    return render(request, 'crmsystem/main.html', {})

def contract_site(request):
    return render(request, 'crmsystem/contract_site.html', {})

def contract_new(request):
    state = "Vytvoriť novú zmluvu"
    if (request.method == "POST"):
        form = ContractForm(request.POST)
        if (form.is_valid()):
            mark = form.save(commit=False)

            # Tu vypocitat celkovu sumu kontraktu
            # podla typu a poctu kusov oblecenia
            mark.total_cost = 5

            mark.save()
            return redirect('contract_site')
        else:
            state = 'Invalid input data'
    else:
        form = ContractForm()

    return render(
        request,
        'crmsystem/contract_new.html',
        {
            'form': form,
            'state': state,
        }
    )

def meeting_site(request):
    mtg_list = Meeting.objects.all()
    return render(
        request,
        'crmsystem/meeting_site.html',
        {
            'list': mtg_list
        }
    )

def meeting_new(request):
    state = "Create new meeting"
    if (request.method == "POST"):
        form = MeetingForm(request.POST)
        if (form.is_valid()):
            mtg = form.save(commit=False)
            mtg.save()
            return redirect('meeting_site')
        else:
            state = "Invalid input data"
    else:
        form = MeetingForm()

    return render(
        request,
        'crmsystem/meeting_new.html',
        {
            'form': form,
            'state': state
        }
    )

def customer_site(request):
    all_customers = Customer.objects.all()
    customer_list = [
        (cust, str(count))
        for cust, count in zip(all_customers, range(0, len(all_customers)))
    ]
    return render(
        request,
        'crmsystem/customer_site.html',
        {
            'list': customer_list
        }
    )

def customer_edit(request, pk):
    return render(request, 'crmsystem/customer_detail.html', {'pk': pk})

def customer_new(request):
    def createCustomer(form):
        # TODO
        # employee_id
        return Customer(
            email=form.cleaned_data.get('email'),
            city=form.cleaned_data.get('city_name'),
            street_number=form.cleaned_data.get('street_number'),
            street_name=form.cleaned_data.get('street_name'),
            telephone_number=form.cleaned_data.get('telephone_number'),
            employee_id=1
        )

    def createLegalPerson(form, customer):
        # TODO
        # domysliet psychical_person column
        return Legal_person(
            ico=form.cleaned_data.get('ico'),
            name=form.cleaned_data.get('name'),
            customer=customer,
            physical_person_id=1
        )

    state = 'Nový zákaznik'
    checked = False

    if (request.method == "POST"):
        form_1 = CustomerForm(request.POST)
        form_2 = Legal_personForm(request.POST)

        if ('legalperson' in request.POST):
            checked = True
            if (form_1.is_valid() and form_2.is_valid()):
                customer = createCustomer(form_1)
                legal_person = createLegalPerson(form_2, customer)
                customer.save()
                legal_person.save()
                return redirect('customer_site')
        else:
            if (form_1.is_valid()):
                createCustomer(form_1).save()
                return redirect('customer_site')

        state = "Invalid input data"
    else:
        form_1 = CustomerForm()
        form_2 = Legal_personForm()

    return render(
        request,
        'crmsystem/customer_new.html',
        {
            'form_1': form_1,
            'form_2': form_2,
            'state': state,
            'checked': checked
        }
    )

def employee_site(request):
    employee_list = Employee.objects.all()
    return render(
        request,
        'crmsystem/employee_site.html',
        {
            'list': employee_list
        }
    )

def employee_new(request):
    state = "Register new employee"
    if (request.method == "POST"):
        form = EmployeeForm(request.POST)
        if (form.is_valid()):
            employee = form.save(commit=False)
            employee.save()
            return redirect('employee_site')
        else:
            state = 'Invalid input data'
    else:
        form = EmployeeForm()

    return render(
        request,
        'crmsystem/employee_new.html',
        {
            'form': form,
            'state': state,
        }
    )

def employee_edit(request, pk):
    return render(request, 'crmsystem/employee_detail.html', {'pk': pk})

def cloth_site(request):
    marks = Mark.objects.all().order_by('name_of_mark')
    clothes = Cloth.objects.all().order_by('name')
    return render(
        request,
        'crmsystem/cloth_site.html',
        {
            'marks': marks,
            'clothes': clothes
        }
    )

def cloth_settings(request):
    marks = Mark.objects.all().order_by('name_of_mark')
    clothes = Cloth.objects.all().order_by('name')  
    return render(
        request,
        'crmsystem/cloth_settings.html',
        {
            'marks': marks,
            'clothes': clothes
        }
    )

# TODO
# Cez modálne okno to urobit v 'cloth_settings.html'
def cloth_new(request):
    state = "Register new cloth"
    if (request.method == "POST"):
        form = ClothForm(request.POST)
        if (form.is_valid()):
            mark = form.save(commit=False)
            mark.save()
            return redirect('cloth_settings')
        else:
            state = 'Invalid input data'
    else:
        form = ClothForm()

    return render(
        request,
        'crmsystem/cloth_new.html',
        {
            'form': form
        }
    )

def mark_new(request):
    state = "Register new mark"
    if (request.method == "POST"):
        form = MarkForm(request.POST)
        if (form.is_valid()):
            mark = form.save(commit=False)
            mark.save()
            return redirect('cloth_settings')
        else:
            state = 'Invalid input data'
    else:
        form = MarkForm()

    return render(
        request,
        'crmsystem/mark_new.html',
        {
            'form': form
        }
    )

def login_form(request):
    state = "Please log in."
    username = password = ''

    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if (user is not None):
            if (user.is_active):
                login(request, user)
                state = "You're successfully logged in!"
                return redirect('default_web')
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username or password were incorrect."

    return render(request, 'account/login.html', {
        'state': state
    })

def logout_form(request):
    logout(request)
    return render(request, 'account/logout.html', {})

def registration_form(request):
    # TODO
    state = 'Welcome !!!!'
    com_owner_group = 'test'
    cus_ser_group = 'test_2'

    if (request.method == "POST"):
        form = RegistrationForm(request.POST)

        # Registration form is valid
        if (form.is_valid()):
            role = form.cleaned_data.get('roles')
            if (role == 'com_owner'):
                group = Group.objects.get(name=com_owner_group)

                # If group is empty, create user
                if (not group.user_set.all()):
                    user = User.objects.create_user(
                        username=form.cleaned_data.get('user_name'),
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name'),
                        email=form.cleaned_data.get('email'),
                        password=form.cleaned_data.get('password2')
                        )
                    user.groups.add(group)

                    return redirect('login_form')
                else:
                    state = 'Company owner is already registered !!!'
            elif (role == 'cus_ser'):
                group = Group.objects.get(name=cus_ser_group)

                # If group is empty, create user
                if (not group.user_set.all()):
                    user = User.objects.create_user(
                        username=form.cleaned_data.get('user_name'),
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name'),
                        email=form.cleaned_data.get('email'),
                        password=form.cleaned_data.get('password2')
                        )
                    user.groups.add(group)

                    return redirect('login_form')
                else:
                    state = 'Customer service is already registered !!!'
            else:
                state = 'Invalid role'
    else:
        form = RegistrationForm()

    return render(request, 'account/registration.html', {
        'form': form,
        'state': state,
    })
