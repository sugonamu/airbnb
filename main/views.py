import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import  PropertyForm
from .models import Property


def home(request):
    if not request.user.is_authenticated:
        return redirect('main:login')
    properties = Property.objects.order_by('?')[:6]  # Featured properties
    user_properties = request.user.properties.all()  # User's properties
    return render(request, 'home.html', {
        'properties': properties,
        'user_properties': user_properties,
        'last_login': request.COOKIES.get('last_login')
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Pass request and data
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = redirect('main:home')
                response.set_cookie('last_login', str(datetime.datetime.now()))  # Optionally set last_login cookie
                return response
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()  # Create a new instance of the form

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
            property_instance = form.save(commit=False)  # Save but don't commit yet
            property_instance.host = request.user  # Set the user as the host
            property_instance.save()  # Now save the property
            return redirect('main:home')  
    else:
        form = PropertyForm()
    return render(request, 'addproperty.html', {'form': form})
    
@login_required
def edit_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id, host=request.user)  # Ensure only the host can edit

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect('main:my_properties')  # Redirect to a user-specific properties page
    else:
        form = PropertyForm(instance=property_instance)

    return render(request, 'editproperty.html', {'form': form})


@login_required
def delete_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id, host=request.user)  # Ensure only the host can delete
    property_instance.delete()
    messages.success(request, "Property deleted successfully.")
    return redirect('main:my_properties')  # Redirect to a user-specific properties page


def property_list(request):
    properties = request.user.properties.all() 
    return render(request, 'property_list.html', {'properties': properties})

