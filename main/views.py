import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.urls import reverse
from .forms import  PropertyForm
from .models import Property, User


def home(request):
    if not request.user.is_authenticated:
        return redirect('main:login')
    properties = Property.objects.order_by('?')[:6]
    user_properties = request.user.properties.all()  
    return render(request, 'home.html', {
        'properties': properties,
        'user_properties': user_properties,
        'last_login': request.COOKIES.get('last_login')
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = redirect('main:home')
                response.set_cookie('last_login', str(datetime.datetime.now())) 
                return response
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm() 

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
    auth_logout(request)
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
            property_instance = form.save(commit=False)  
            property_instance.host = request.user  
            property_instance.save() 
            return redirect('main:home')  
    else:
        form = PropertyForm()
    return render(request, 'addproperty.html', {'form': form})
    
@login_required
def edit_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id, host=request.user) 

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect('main:property_list')  
    else:
        form = PropertyForm(instance=property_instance)

    return render(request, 'editproperty.html', {'form': form})


def delete_property(request, product_id):
    property_instance = get_object_or_404(Property, id=product_id)  # Use id for UUID
    property_instance.delete()
    return HttpResponseRedirect(reverse('main:home'))

def property_list(request):
    properties = request.user.properties.all() 
    return render(request, 'property_list.html', {'properties': properties})

@login_required
def user_list(request):
    # Replace 'your_username' with your actual username
    if request.user.username != 'fact':
        return HttpResponseForbidden("You are not allowed to view this page.")
    
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})