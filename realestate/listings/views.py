from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Property,PropertyType,Location
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse
# Create your views here.
def home(request):
    properties = Property.objects.all()
    return render(request,'home.html',{'properties':properties})

def base(request):
    return render(request,'base.html')



def search_results(request):
    query = request.GET.get('q')
    location = request.GET.get('location')
    property_type = request.GET.get('property_type')
    price_max = request.GET.get('price_max')

    properties = Property.objects.all()

    if query:
        properties = properties.filter(title__icontains=query)
    if location:
        properties = properties.filter(location__city__icontains=location)
    if property_type:
        properties = properties.filter(property_type__name__icontains=property_type)
    if price_max:
        properties = properties.filter(price__lte=price_max)

    context = {
        'properties': properties,
    }

    return render(request, 'search_results.html', context)


@login_required
def property_details(request):
    properties = Property.objects.all()
    locations = Location.objects.all()
    property_types = PropertyType.objects.all()
    favorites = request.session.get('favorites', [])

    context = {
        'properties': properties,
        'locations': locations,
        'property_types': property_types,
        'favorites': favorites,
    }
    return render(request, 'property_details.html', context)


from django.http import JsonResponse


def favorites(request):
    if request.method == 'POST':
        property_id = request.POST.get('property_id')

        if not property_id.isdigit():
            return JsonResponse({'status': 'error', 'message': 'Invalid property ID'})

        property_id = int(property_id)
        favorites = request.session.get('favorites', [])

        if property_id in favorites:
            favorites.remove(property_id)
            status = 'removed'
        else:
            favorites.append(property_id)
            status = 'added'

        request.session['favorites'] = favorites
        return JsonResponse({'status': status})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




def house_list(request):
    houses = Property.objects.filter(property_type__name='House')
    return render(request,'house_list.html',{'houses':houses})


def apartment_list(request):
    apartments = Property.objects.filter(property_type__name='Apartment')
    return render(request, 'apartment_list.html', {'apartments': apartments})


def land_list(request):
    lands = Property.objects.filter(property_type__name='Land')
    return render(request,'land_list.html',{'lands':lands})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        email = request.POST.get('email', '')


        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')


        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        try:

            myuser = User.objects.create_user(username=username, password=password1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.email = email
            myuser.save()
            messages.success(request, 'Account created successfully')
            return redirect('signin')
        except IntegrityError:
            messages.error(request, 'An error occurred. Please try again.')
            return redirect('signup')

    return render(request, 'signup.html')



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('property_details')  # Redirect to property_details page after login
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')

    return render(request, 'signin.html')



def signout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('signin')

def about(request):
    return render(request,'about.html')

def contacts(request):
    return render(request,'contacts.html')