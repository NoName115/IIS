from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *


def default_web(request):
    return render(request, 'crmsystem/main.html', {})

def no_permission(request):
    return render(request, 'account/no_permission.html', {})

@permission_required(
    'crmsystem.show_contract',
    login_url='/accounts/nopermission/'
)
def contract_site(request):
    contract_list = Contract.objects.all()
    return render(
        request,
        'crmsystem/contract_site.html',
        {
            'list': contract_list,
        }
    )

@permission_required(
    'crmsystem.add_contract',
    login_url='/accounts/nopermission/'
)
def contract_new(request):
    def is_productlist_ok(request_post):
        keys_dict = {}
        form_list = []
        all_valid = True

        # Filter keys from POST
        for key, value in request_post.items():
            if ((nop_name in key) or (cloth_name in key)):
                keys_dict.update({
                    key: value
                })

        # Get maximum index
        maximum = max(
            [int(key.split(delimiter)[1]) for key in keys_dict]
        )

        # Create dictionaries for forms
        for i in range(0, maximum + 1):
            form_dict = {
                nop_name: request_post[nop_name + delimiter + str(i)],
                cloth_name: request_post[cloth_name + delimiter + str(i)],
            }
            new_containform = ContainForm(form_dict)
            form_list.append(
                (
                    new_containform,
                    i,
                    int(form_dict[cloth_name]) if (form_dict[cloth_name]) else 0
                )
            )

            if (not new_containform.is_valid()):
                all_valid = False

        return {
            'is_valid': all_valid,
            'form_list': form_list,
            'maximum': maximum,
        }

    state = "Vytvoriť novú zmluvu"
    nop_name = 'num_of_pieces'
    cloth_name = 'cloth'
    delimiter = '__'
    show_validation = True

    if (request.method == "POST"):
        contract_form = ContractForm(request.POST)

        # Remove last product
        if ('remove_product' in request.POST):
            show_validation = False
            product_dict = is_productlist_ok(request.POST)
            product_dict['form_list'] = product_dict['form_list'][:-1]
        # Add new product
        elif ('add_product' in request.POST):
            show_validation = False
            product_dict = is_productlist_ok(request.POST)

            if (product_dict['is_valid']):
                product_dict['form_list'].append(
                    (ContainForm(), product_dict['maximum'] + 1, 0)
                )
        else:
            # Only check form_list
            product_dict = is_productlist_ok(request.POST)

            if (product_dict['is_valid'] and
               contract_form.is_valid() and
               len(product_dict['form_list']) >= 1):
                contract = contract_form.save(commit=False)

                # Calculate total price
                total_price = 0.0
                contain_list = []
                for product_tuple in product_dict['form_list']:
                    contain = product_tuple[0].save(commit=False)
                    total_price += float(contain.cloth.cost_of_piece)
                    contain_list.append(contain)

                print(request.user)

                contract.employee = Employee.objects.filter(
                    user_account=request.user
                )[0]
                contract.total_cost = total_price
                contract.save()

                for contain in contain_list:
                    contain.contract = contract
                    contain.save()

                return redirect('contract_site')

        form_list = product_dict['form_list']
    else:
        contract_form = ContractForm()
        form_list = [
            (ContainForm(), 0, 0),
        ]

    return render(
        request,
        'crmsystem/contract_new.html',
        {
            'form_1': contract_form,
            'form_list': form_list,
            'state': state,
            'show_validation': show_validation,
        }
    )

@permission_required(
    'crmsystem.delete_contract',
    login_url='/accounts/nopermission/'
)
def contract_delete(request, pk):
    contract_object = get_object_or_404(Contract, pk=pk)
    contract_object.delete()
    return redirect('contract_site')

@permission_required(
    'crmsystem.show_meeting',
    login_url='/accounts/nopermission/'
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

@permission_required(
    'crmsystem.add_meeting',
    login_url='/accounts/nopermission/'
)
def meeting_new(request):
    state = "Nové stretnutie"

    if (request.method == "POST"):
        form = MeetingForm(request.POST)
        if (form.is_valid()):
            mtg = form.save(commit=False)
            mtg.employee = Employee.objects.filter(
                    user_account=request.user
            )[0]
            mtg.save()
            return redirect('meeting_site')
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

@permission_required(
    'crmsystem.show_customer',
    login_url='/accounts/nopermission/'
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


@permission_required(
    'crmsystem.change_customer',
    login_url='/accounts/nopermission/'
)
def customer_edit(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)

    contain_legalperson = False
    if (not customer_object.legal_person_id is None):
        legalperson_object = get_object_or_404(
            Legal_person,
            pk=customer_object.legal_person.pk
        )
        contain_legalperson = True

    state = "Úprava zákaznika"
    isEmployee = False
    # Check if user is Employee or Service
    isEmployee = request.user.groups.filter(
        name='Employee_group'
    ).exists()

    if (request.method == "POST"):
        form_1 = CustomerForm(request.POST, instance=customer_object)

        if (isEmployee):
            # Remove employee field assign from form_1
            form_1.fields.pop('employee')

        # Form is valid, # Only one error, email exist
        if ('email' in form_1.errors and len(form_1.errors) == 1):
            customer_object.name = form_1.cleaned_data.get('name')
            customer_object.surname = form_1.cleaned_data.get('surname')
            customer_object.city = form_1.cleaned_data.get('city')
            customer_object.street_number = form_1.cleaned_data.get('street_number')
            customer_object.street_name = form_1.cleaned_data.get('street_name')
            customer_object.telephone_number = form_1.cleaned_data.get('telephone_number')
            if (not isEmployee and 'employee' in request.POST):
                customer_object.employee = form_1.cleaned_data.get('employee')

            customer_object.save()
            return redirect('customer_site')
    else:
        form_1 = CustomerForm(instance=customer_object)
        if (isEmployee):
            form_1.fields.pop('employee')

    if (contain_legalperson):
        form_2 = Legal_personForm(instance=legalperson_object)

    # Remove pk(email) from form_1
    form_1.fields.pop('email')

    # Create dictionary for html
    out_dict = {
        'form_1': form_1,
        'state': state,
    }
    if (contain_legalperson):
        out_dict.update({
            'form_2': form_2,
            'editable': True,
            'locked': True,
        })

    return render(
        request,
        'crmsystem/customer_new.html',
        out_dict
    )

@permission_required(
    'crmsystem.add_customer',
    login_url='/accounts/nopermission/'
)
def customer_new(request):
    def createCustomer(form, legal_person):
        return Customer(
            email=form.cleaned_data.get('email'),
            name=form.cleaned_data.get('name'),
            surname=form.cleaned_data.get('surname'),
            city=form.cleaned_data.get('city'),
            street_number=form.cleaned_data.get('street_number'),
            street_name=form.cleaned_data.get('street_name'),
            telephone_number=form.cleaned_data.get('telephone_number'),
            employee=form.cleaned_data.get('employee'),
            legal_person=legal_person
        )

    def createLegalPerson(form):
        return Legal_person(
            ico=form.cleaned_data.get('ico'),
            company_name=form.cleaned_data.get('company_name'),
        )

    state = 'Nový zákaznik'
    checked = False

    if (request.method == "POST"):
        form_1 = CustomerForm(request.POST)
        form_2 = Legal_personForm(request.POST)

        if ('legalperson' in request.POST):
            checked = True
            if (form_1.is_valid() and form_2.is_valid()):
                legal_person = createLegalPerson(form_2)
                customer = createCustomer(form_1, legal_person)
                legal_person.save()
                customer.save()
                return redirect('customer_site')
        else:
            if (form_1.is_valid()):
                createCustomer(form_1, None).save()
                return redirect('customer_site')
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

@permission_required(
    'crmsystem.show_employee',
    login_url='/accounts/nopermission/'
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

@permission_required(
    'crmsystem.add_employee',
    login_url='/accounts/nopermission/'
)
def employee_new(request):
    # TODO
    # Vyber znaciek dorobit
    state = "Nový zamestnanec"

    if (request.method == "POST"):
        form = EmployeeForm(request.POST)
        if (form.is_valid()):
            # Create new user
            username = request.POST['username']
            employee_user = User.objects.create_user(
                username,
                username + '@vobec.nic',
                '123' + username.lower() + '321'
            )
            employee_user.groups.add(Group.objects.get(name='Employee_group'))

            employee = form.save(commit=False)
            employee.user_account = employee_user
            employee.save()
            return redirect('employee_site')
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

@permission_required(
    'crmsystem.change_employee',
    login_url='/accounts/nopermission/'
)
def employee_edit(request, pk):
    employee_object = get_object_or_404(Employee, pk=pk)
    if (request.method == "POST"):
        form = EmployeeForm(request.POST, instance=employee_object)
        if (form.is_valid()):
            form.save()
            return redirect('employee_site')
    else:
        form = EmployeeForm(instance=employee_object)

    return render(request, 'crmsystem/employee_new.html', {'form': form})

@permission_required(
    'crmsystem.show_cloth',
    login_url='/accounts/nopermission/'
)
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

@permission_required(
    'crmsystem.add_cloth',
    login_url='/accounts/nopermission/'
)
def cloth_new(request, pk):
    mark_object = get_object_or_404(Mark, pk=pk)
    state = "Nové oblečenie pre značku: " + mark_object.name_of_mark

    if (request.method == "POST"):
        form = ClothForm(request.POST)
        if (form.is_valid()):
            new_cloth = form.save(commit=False)
            new_cloth.mark = mark_object
            new_cloth.save()
            return redirect('cloth_site')
    else:
        form = ClothForm()

    return render(
        request,
        'crmsystem/cloth_new.html',
        {
            'form': form,
            'state': state,
        }
    )

@permission_required(
    'crmsystem.add_mark',
    login_url='/accounts/nopermission/'
)
def mark_new(request):
    state = "Register new mark"
    if (request.method == "POST"):
        form = MarkForm(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('cloth_site')
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
