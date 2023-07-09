from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from blood.forms import RequestForm, DonateForm, BloodForm
from blood.models import BloodRequest, BloodDonate, BloodStock
from core import settings
from .forms import UserRegisterForm, LoginForm, DonorForm
from .models import Account
from django.db.models import Count, Case, When


#  ---------- User Register and sigh_in ----------

def register(request):
    if request.method == 'POST':
        forms = UserRegisterForm(request.POST, request.FILES)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.set_password(
                forms.cleaned_data["password"]
            )
            user.save()
            user = authenticate(request, email=forms.cleaned_data['email'], password=forms.cleaned_data['password'])
            print(forms.cleaned_data['email'], forms.cleaned_data['password'])
            if user:
                login(request, user)
            else:
                forms = UserRegisterForm()
                return render(request, 'register_form.html', {'form': forms})

            if user.is_donor:
                return HttpResponseRedirect(f'{settings.BASE_URL}/donor/dashboard')
            else:
                return HttpResponseRedirect(f'{settings.BASE_URL}/patient/dashboard')
        else:
            return render(request, 'register_form.html', {'form': forms})
    else:
        forms = UserRegisterForm()
        return render(request, 'register_form.html', {'form': forms})


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login_form.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user and not user.is_donor and not user.is_admin:
                login(request, user)
                return HttpResponseRedirect(f'{settings.BASE_URL}/patient/dashboard')
            if user and user.is_donor and not user.is_admin:
                login(request, user)
                return HttpResponseRedirect(f'{settings.BASE_URL}/donor/donate')
            if user and user.is_admin:
                login(request, user)
                return HttpResponseRedirect(f'{settings.BASE_URL}/admin-dashboard')

        return render(request, 'login_form.html', {'form': form})


#  ---------- Patient views and functionality ----------


def pat_dashboard(request):
    if not request.user.is_donor:
        queryset = BloodRequest.objects.filter(request_by_patient=request.user).aggregate(
            request_pending=Count(Case(When(status='Pending', then=1))),
            request_approved=Count(Case(When(status='Approved', then=1))),
            request_made=Count('id'),
            request_rejected=Count(Case(When(status='Rejected', then=1))),
        )

        context = {
            'request_pending': queryset['request_pending'],
            'request_approved': queryset['request_approved'],
            'request_made': queryset['request_made'],
            'request_rejected': queryset['request_rejected'],
        }

        return render(request, 'patient/pat_dash.html', context)


def make_request(request):
    request_form = RequestForm()
    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            blood_request = request_form.save(commit=False)
            blood_request.blood_group = request.user.blood_group
            blood_request.patient_name = request.user.first_name
            blood_request.patient_age = request.user.age
            patient = Account.objects.get(id=request.user.id)
            blood_request.request_by_patient = patient
            blood_request.save()
            return HttpResponseRedirect(f'{settings.BASE_URL}/patient/my-request')

    return render(request, 'patient/make_request.html', {'form': request_form})


def my_request_view(request):
    blood_request = BloodRequest.objects.all().filter(request_by_patient=request.user)
    return render(request, 'patient/my_request.html', {'context': blood_request})


def log_out(request):
    logout(request)
    return render(request, 'index.html')


#  ---------- Donor views and functionality ----------


def donate_blood(request):
    donation_form = DonateForm()
    if request.method == 'POST':
        donation_form = DonateForm(request.POST)
        if donation_form.is_valid():
            print('valid')
            blood_donate = donation_form.save(commit=False)
            blood_donate.blood_group = request.user.blood_group
            blood_donate.donor_name = request.user.first_name
            blood_donate.donor_age = request.user.age
            if request.user.disease:
                blood_donate.disease = request.POST['disease'] + request.user.disease
            elif request.POST['disease']:
                blood_donate.disease = request.POST['disease']
            donor = Account.objects.get(id=request.user.id)
            blood_donate.donor = donor
            blood_donate.save()
            return HttpResponseRedirect(f'{settings.BASE_URL}donor/dashboard')
    return render(request, 'donor/donate_blood.html', {'form': donation_form})


def donor_dashboard(request):
    donations = BloodDonate.objects.all().filter(donor=request.user)
    return render(request, 'donor/donor_dashboard.html', {'donations': donations})


def donor_patients(request):
    blood_requests = BloodRequest.objects.select_related('request_by_patient').all()

    return render(request, 'donor/donor_patients.html', {'patients': blood_requests})


# ------------- Admin------------

def get_blood_stock():
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    blood_stock = BloodStock.objects.filter(blood_group__in=blood_groups)

    blood_stock_dict = {blood.blood_group: blood.amount for blood in blood_stock}

    context = {

        'A1': blood_stock_dict.get("A+"),
        'A2': blood_stock_dict.get("A-"),
        'B1': blood_stock_dict.get("B+"),
        'B2': blood_stock_dict.get("B-"),
        'AB1': blood_stock_dict.get("AB+"),
        'AB2': blood_stock_dict.get("AB-"),
        'O1': blood_stock_dict.get("O+"),
        'O2': blood_stock_dict.get("O-"),
    }
    return context


def admin_dashboard_view(request):
    blood_stock = get_blood_stock()
    total_amount = 0
    for key, value in blood_stock.items():
        print(key, value)
        total_amount += value
    context = blood_stock | {
        'totaldonors': Account.objects.filter(is_donor=True).all().count(),
        'totalbloodunit': total_amount,
        'totalrequest': BloodRequest.objects.all().count(),
        'totalapprovedrequest': BloodRequest.objects.all().filter(status='Approved').count()
    }
    return render(request, 'admin/dashboard.html', context=context)


def update_blood_amount(request):
    form = {'blood_form': BloodForm()} | get_blood_stock()
    print(form)

    if request.method == 'POST':
        blood_form = BloodForm(request.POST)
        if blood_form.is_valid():
            blood_group = blood_form.cleaned_data['blood_group']
            blood_stock = BloodStock.objects.get(blood_group=blood_group)
            blood_stock.amount = blood_form.cleaned_data['amount']
            blood_stock.save()
        return HttpResponseRedirect('blood-update')
    return render(request, 'admin/blood_update.html', form)


def admin_donor_view(request):
    donors = Account.objects.filter(is_donor=True).all()
    return render(request, 'admin/admin-donor.html', {'users': donors, 'us': 'Donors List'})


def update_user_view(request, pk):
    user = Account.objects.get(id=pk)
    donor_form = DonorForm(request.POST, request.FILES, instance=user)
    mydict = {'donorForm': donor_form}
    if user.is_donor:
        mydict = mydict | {'us': 'Donor update'}
    else:
        mydict = mydict | {'us': 'Patient update'}

    if request.method == 'POST':
        if donor_form.is_valid():
            user = donor_form.save()
            user.set_password(user.password)
            user.blood_group = donor_form.cleaned_data['blood_group']
            user.save()
            return HttpResponseRedirect(f'{settings.BASE_URL}admin-donor')
    return render(request, 'admin/update-donor.html', mydict)


def delete_donor(request, pk):
    donor = Account.objects.get(id=pk)
    donor.delete()
    return HttpResponseRedirect(f'{settings.BASE_URL}admin-donor')


def admin_patient_view(request):
    patients = Account.objects.filter(is_donor=False).filter(is_admin=False).all()
    return render(request, 'admin/admin-donor.html', {'users': patients, 'us': 'Patients List'})


def admin_request_view(request):
    requests = BloodRequest.objects.all().filter(status='Pending')
    return render(request, 'admin/admin_request.html', {'requests': requests})


def admin_request_history_view(request):
    requests = BloodRequest.objects.all().exclude(status='Pending')
    return render(request, 'admin/admin_request_history.html', {'requests': requests})


def admin_donation_view(request):
    donations = BloodDonate.objects.all()
    return render(request, 'admin/admin_donation.html', {'donations': donations})


def update_approve_status_view(request, pk):
    req = BloodRequest.objects.get(id=pk)
    message = None
    blood_group = req.blood_group
    unit = req.amount
    stock = BloodStock.objects.get(blood_group=blood_group)
    if stock.amount > unit:
        stock.amount = stock.amount - unit
        stock.save()
        req.status = "Approved"

    else:
        message = "Stock Doest Not Have Enough Blood To Approve This Request, Only " + str(
            stock.amount) + " Unit Available"
    req.save()

    requests = BloodRequest.objects.all().filter(status='Pending')
    return render(request, 'admin/admin_request.html', {'requests': requests, 'message': message})


def update_reject_status_view(request, pk):
    req = BloodRequest.objects.get(id=pk)
    req.status = "Rejected"
    req.save()
    return HttpResponseRedirect('/admin-request')


def approve_donation_view(request, pk):
    donation = BloodDonate.objects.get(id=pk)
    donation_blood_group = donation.blood_group
    donation_blood_unit = donation.amount

    stock = BloodStock.objects.get(blood_group=donation_blood_group)
    stock.amount = stock.amount + donation_blood_unit
    stock.save()

    donation.status = 'Approved'
    donation.save()
    return HttpResponseRedirect('/admin-donation')


def reject_donation_view(request, pk):
    donation = BloodDonate.objects.get(id=pk)
    donation.status = 'Rejected'
    donation.save()
    return HttpResponseRedirect('/admin-donation')
