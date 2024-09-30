from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .forms import  PropertyForm
from .models import Property


def home(request):
    properties = Property.objects.order_by('?')[:6]
    return render(request, 'home.html', {'properties': properties})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('main:login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def error(request):
    return render(request, 'error.html') 

def property_detail(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    return render(request, 'property_detail.html', {'property': property_instance})

def add_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.host = request.user 
            property.save()
            return redirect('main:home')  
    else:
        form = PropertyForm()
    return render(request, 'addproperty.html', {'form': form})
    
def edit_property(request, product_id):
    product = Property.objects.get(pk=product_id)

    form = PropertyForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:home'))

    context = {'form': form}
    return render(request, "editproduct.html", context)

def delete_property(request, product_id):
    property = Property.objects.get(pk=product_id)
    property.delete()
    return HttpResponseRedirect(reverse('main:home'))

def property_list(request):
    properties = Property.objects.filter(is_available=True)
    return render(request, 'property_list.html', {'properties': properties})

