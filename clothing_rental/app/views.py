from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AdForm
from .models import Ad
from django.contrib.auth.models import User


def home(request):
    try:
        staff = User.objects.get(username=request.user).is_staff
        context = {'is_staff': staff}
    except Exception:
        context = {'is_staff': False}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'registration/login.html')


def user_logout(request):
    if request.method == 'POST':
        logout(request)
    return render(request, 'home.html')


def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            ad.category.set(form.cleaned_data['category'])
            return redirect('home')
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})


def pending_ads(request):
    user = User.objects.get(username=request.user)
    if not user.is_staff:
        return redirect('home')

    ads = Ad.objects.filter(is_approved=False)
    return render(request, 'ads/approve_ad.html', {'ads': ads})


def approve_ad(request, pk):
    user = User.objects.get(username=request.user)
    if not user.is_staff:
        return redirect('home')
    ad = Ad.objects.get(pk=pk)
    ad.is_approved = True
    ad.save()
    return redirect('pending_ads')


def view_user_ads(request):
    ads = Ad.objects.for_user(request.user)
    context = {'ads': ads}
    return render(request, 'ads/user_ads.html', context)


def remove_ad(request, pk):
    ad = Ad.objects.get_queryset().filter(id=pk)
    ad.delete()
    return redirect('user_ads')


# def edit_ad(request, pk):
#     ad = Ad.objects.get_queryset().filter(id=pk)
#     ad.save()
#     return redirect('user_ads')


#TODO: edit ad
#TODO: order ad