from django.shortcuts import render, redirect
from .models import *
from . forms import CreateUserForm, LoginForm
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
import json

@login_required(login_url='login')
def cabinet(request):
    userMedicines = json.loads(request.user.medicines)
    ids = [int(med["id"]) for med in userMedicines]
    medicines = Medicine.objects.filter(id__in=set(ids))
    med_lookup = {med.id: med for med in medicines}
    result = [med_lookup.get(id) for id in ids]
    result_dicts = [model_to_dict(med) for med in result]
    print(userMedicines)
    print("----------------")
    print(result_dicts)
    for i in range(len(result_dicts)):
        print(result_dicts[i])
        print(userMedicines[i])
        result_dicts[i]['quantity'] = userMedicines[i]["quantity"]
        result_dicts[i]['expiration'] = userMedicines[i]["made_on"]
    print(result_dicts)
    return render(request, 'main/cabinet.html', {
        'medicines': result_dicts
    })
    
@login_required(login_url='login')
def schedule(request):
    medicines = Medicine.objects.all().order_by('name')
    return render(request, 'main/schedule.html', {
        'medicines': medicines
    })
    
@login_required(login_url='login')
def prescriptions(request):
    userid = request.user.id
    
    return render(request, 'main/prescriptions.html',{
        'medicines': Prescriptions.objects.filter(id = userid)
    })

@login_required(login_url='login')
def prescription(request,pk):
    return render(request, 'main/prescription.html',{
        'med': Prescriptions.objects.get(id = pk)
    })

@login_required(login_url='login')
def find_medicine(request):
    medicines = Medicine.objects.all().order_by('name')
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

def MedicineDetail(request,mid):
    if request.method == "POST":
        userMedicines = json.loads(request.user.medicines)
        print("METHOD------------------")
        print(request.method)
        userMedicines.append({"id":str(mid),"made_on":0,"quantity":request.POST['quantity']})
        userMedicines = json.dumps(userMedicines)
        
        user = request.user
        user.medicines = userMedicines
        user.save()
    if request.method == "GET":
        print("hello world")
    return render(request, 'main/medicine_details.html', {
        'medicine': Medicine.objects.get(pk=mid)
    })
    

class MedicineDetailView(DetailView):
    model = Medicine
    template_name = 'main/medicine_details.html'
    
def add_medicine(request, id):
    
    if request.method == "POST":
        userMedicines = json.loads(request.user.medicines)
        print("METHOD------------------")
        print(request.method)
        userMedicines.append({"id":str(id),"made_on":0,"quantity":request.POST['quantity']})
        userMedicines = json.dumps(userMedicines)
        
        user = request.user
        user.medicines = userMedicines
        user.save()
    return redirect('cabinet')