from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AdForm, SearchAdForm, CommentAdForm, OrderForm
from .models import Ad, Category, AdComments, Transaction
from django.contrib.auth.models import User
from django.db.models import Q
from functools import reduce
import operator


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
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        logout(request)
    return render(request, 'home.html')


def create_ad(request):
    if not request.user.is_authenticated:
        return redirect('home')
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
    if not request.user.is_authenticated:
        return redirect('home')
    user = User.objects.get(username=request.user)
    if not user.is_staff:
        return redirect('home')

    ads = Ad.objects.filter(is_approved=False)
    return render(request, 'ads/approve_ad.html', {'ads': ads})


def approve_ad(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
    user = User.objects.get(username=request.user)
    if not user.is_staff:
        return redirect('home')
    ad = Ad.objects.get(pk=pk)
    ad.is_approved = True
    ad.save()
    return redirect('pending_ads')


def pending_comments(request):
    if not request.user.is_authenticated:
        return redirect('home')
    user = User.objects.get(username=request.user)
    if not user.is_staff:
        return redirect('home')

    comments = AdComments.objects.filter(is_approved=False)
    return render(request, 'ads/pending_comments.html', {'comments': comments})


def approve_comment(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
    user = User.objects.get(username=request.user)
    if not user.is_staff:
        return redirect('home')
    comment = AdComments.objects.get(pk=pk)
    comment.is_approved = True
    comment.save()
    return redirect('pending_comments')


def view_user_ads(request):
    if not request.user.is_authenticated:
        return redirect('home')
    ads = Ad.objects.for_user(request.user)
    context = {'ads': ads}
    return render(request, 'ads/user_ads.html', context)


def remove_ad(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
    ad = Ad.objects.get(pk=pk)
    if ad.user != request.user:
        return redirect('home')
    ad.delete()
    return redirect('user_ads')


def edit_ad(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
    ad = Ad.objects.get(pk=pk)
    if ad.user != request.user:
        return redirect('home')
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.is_approved=False
            ad.save()
            ad.category.set(form.cleaned_data['category'])
            return redirect('user_ads')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/create_ad.html', {'form': form})


def search_ads(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SearchAdForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['categories'] if form.cleaned_data['categories'] else Category.objects.all()
            min_price = form.cleaned_data['min_price'] if form.cleaned_data['min_price'] else 0
            max_price = form.cleaned_data['max_price'] if form.cleaned_data['max_price'] else 99999.99
            keywords = form.cleaned_data['keywords'].split() if form.cleaned_data['keywords'] else ['']
            keyword_q = reduce(operator.or_, (Q(name__icontains=keyword) | Q(description__icontains=keyword) for keyword in keywords))
            ads = (Ad.objects
                   .filter(is_approved=True,
                           category__in=categories,
                           price__gte=min_price,
                           price__lte=max_price)
                   .filter(keyword_q)
                   .distinct())
            context = {'ads': ads, 'form': form}
            return render(request, 'ads/search_ads.html', context)
    else:
        form = SearchAdForm()
    return render(request, 'ads/search_ads.html', {'form': form})


def view_ad(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
    ad = Ad.objects.get(pk=pk)
    comments = AdComments.objects.filter(ad=ad, is_approved=True)
    if request.method == 'POST':
        comment_form = CommentAdForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ad = ad
            comment.user = request.user
            comment.save()
            return redirect('view_ad', pk)
    else:
        comment_form = CommentAdForm()
    context = {'ad': ad, 'comment_form': comment_form, 'comments': comments}
    return render(request, 'ads/view_ad.html', context)


def order_ad(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
    ad = Ad.objects.get(pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            if ad.start_date > form.cleaned_data['start_date'] or ad.end_date < form.cleaned_data['end_date']:
                message = f'The dates must be in range {ad.start_date} - {ad.end_date}'
                context = {'form': form, 'message': message}
                return render(request, 'ads/order_ad.html', context)
            order = form.save(commit=False)
            order.ad = ad
            order.user = request.user
            order.save()
            transaction = Transaction.objects.create(user=request.user, order=order, total_price=order.quantity*ad.price)
            return redirect('view_ad', pk)
    else:
        form = OrderForm()
    context = {'form': form}
    return render(request, 'ads/order_ad.html', context)


#TODO: Docker