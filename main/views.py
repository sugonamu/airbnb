from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, ReservationForm, ReviewForm
from .models import Property, Reservation, Review  # Import your Property, Reservation, and Review models

# Home page view
def home(request):
    properties = Property.objects.filter(is_available=True)[:6]  # Limit to 6 featured properties
    return render(request, 'home.html', {'properties': properties})

# Property list view
def property_list(request):
    properties = Property.objects.filter(is_available=True)
    return render(request, 'property_list.html', {'properties': properties})

# Property detail view
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    images = property.images.all()  # Assuming a ForeignKey or related name for images
    amenities = property.amenities.all()  # Assuming a ManyToMany or related name for amenities
    return render(request, 'property_detail.html', {
        'property': property,
        'images': images,
        'amenities': amenities,
    })

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set hashed password
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# Reservation view
@login_required
def make_reservation(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.guest = request.user
            reservation.property = property
            reservation.total_price = (reservation.check_out - reservation.check_in).days * property.price_per_night
            reservation.save()
            messages.success(request, "Reservation successful!")
            return redirect('reservation_detail', reservation_id=reservation.id)
    else:
        form = ReservationForm()
    return render(request, 'make_reservation.html', {'form': form, 'property': property})

# View to see reservation details
@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation': reservation})

# View to leave a review for a property (linked to a reservation)
@login_required
def leave_review(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reservation = reservation
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('property_detail', property_id=reservation.property.id)
    else:
        form = ReviewForm()
    return render(request, 'leave_review.html', {'form': form, 'reservation': reservation})

# View to see all reviews for a property
def property_reviews(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    reviews = Review.objects.filter(reservation__property=property)
    return render(request, 'property_reviews.html', {'property': property, 'reviews': reviews})
