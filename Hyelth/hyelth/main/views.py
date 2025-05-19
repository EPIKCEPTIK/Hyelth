from django.shortcuts import render, redirect
from .models import Medicine, MedicineDetail
from . forms import CreateUserForm, LoginForm
from django.views.generic.detail import DetailView
from django.contrib.auth.models import  auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

@login_required(login_url='login')
def cabinet(request):
    medicines = Medicine.objects.all().order_by('name')
    return render(request, 'main/cabinet.html', {
        'medicines': medicines
    })
    
@login_required(login_url='login')
def schedule(request):
    medicines = Medicine.objects.all().order_by('name')
    return render(request, 'main/schedule.html', {
        'medicines': medicines
    })
    
@login_required(login_url='login')
def prescriptions(request):
    return render(request, 'main/prescriptions.html')

@login_required(login_url='login')
def find_medicine(request):
    medicines = MedicineDetail.objects.all().order_by('name')
    return render(request, 'main/find_medicine.html', {
        'medicines': medicines
    })


def registration(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    context = {'registration_form': form}

    return render(request, 'main/register.html',context=context)

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request ,data = request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('cabinet')
    context = {'login_form': form}
    return render(request, 'main/login.html', context=context)

def user_logout(request):
    auth.logout(request)
    return redirect('login')

class MedicineDetailView(DetailView):
    model = MedicineDetail
    template_name = 'main/medicine_details.html'