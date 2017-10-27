##################################################
# Run this script before first running of server #
#           but after migration  !!!             #
##################################################

from django.contrib.auth.models import Group, Permission, User


def create_group(name):
    # Group creation
    new_group, created = Group.objects.get_or_create(name=name)
    if (not created):
        print('Group: ' + name + " has already been created")

    return new_group, created

def assign_permissions(permission_codename_list, group):
    for permission_codename in permission_codename_list:
        print(permission_codename)
        group.permissions.add(
            Permission.objects.get(codename=permission_codename)
        )

def main():
    employee_group_name = 'Employee_group'
    customerservice_group_name = 'Customerservice_group'
    companyowner_group_name = 'Companyowner_group'

    # Creation of 3 main groups
    employee_group, employee_created = create_group(employee_group_name)
    customerservice_group, customerservice_created = create_group(customerservice_group_name)
    companyowner_group, companyowner_created = create_group(companyowner_group_name)

    if (employee_created):
        assign_permissions(
            [
                'edit_customer_info', 'show_customer',
                'show_mark', 'show_cloth',
                'add_contract', 'delete_contract', 'show_contract',
                'add_meeting', 'show_meeting',
            ],
            employee_group
        )

    if (customerservice_created):
        assign_permissions(
            [
                'add_employee', 'change_employee', 'show_employee',
                'add_mark',
                'add_customer', 'assign_employee',
                'show_mark', 'add_mark',
                'show_cloth', 'add_cloth',

            ],
            customerservice_group
        )
    
    if (companyowner_created):
        assign_permissions(
            [
                'show_employee',
                'show_customer',
                'show_mark',
                'show_cloth',
                'show_contract',
                'show_meeting',
            ],
            companyowner_group
        )

    try:
        test = User.objects.get(username='Service')
    except User.DoesNotExist:
        customer_service = User.objects.create_user('Service', 'service@vobec.nic', '123service321')
        customer_service.groups.add(customerservice_group)

    try:
        test = User.objects.get(username='Owner')
    except User.DoesNotExist:
        company_owner = User.objects.create_user('Owner', 'owner@vobec.nic', '123owner321')
        company_owner.groups.add(companyowner_group)
