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
        dateMade = userMedicines[i]["made_on"]
        expiration = Medicine.objects.get(id = userMedicines[i]["id"]).expiration
        dateMade = dateMade.split(".")
        expiration = expiration.split(".")
        dates = [str(int(dateMade[i])+int(expiration[i])) for i in range(3)]
        for m in range(len(dates)):
            dates[m] = "0"+ dates[m] if len(dates[m])<=1 else dates[m]
        resexp = ".".join(dates)
        result_dicts[i]['expiration'] = resexp
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
    prescriptionsList = Prescriptions.objects.filter(userID = request.user.id)
    result = [{
                'id':med.id,
                'number':med.number,
                'doctorName':med.prescribedBy,
                'medicines':', '.join({(Medicine.objects.get(id=s['id']).name) for s in json.loads(med.medicines)})
                } for med in prescriptionsList]
    n = 30
    for med in result:
        if(len(med['medicines']) > n):
            med['medicines'] = med['medicines'][:n-3]+"..."
    return render(request, 'main/prescriptions.html',{
        'medicines': result
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
        userMedicines.append({"id":str(mid),"made_on":"0000.00.00","quantity":request.POST['quantity']})
        userMedicines = json.dumps(userMedicines)
        
        user = request.user
        user.medicines = userMedicines
        user.save()
    if request.method == "GET":
        print("hello world")
    return render(request, 'main/medicine_details.html', {
        'medicine': Medicine.objects.get(pk=mid)
    })
    
    
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