from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from contacts.models import Contact


def index(request):
    return redirect('login')


def register(request):
    if request.method == 'POST':
        #regiter user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register') 
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register') 
        else:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email)

            user.save();
            messages.success(request, 'Your are now registered. Please login')
            return redirect('login')
        
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,
                                password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('dashboard')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Successfully logged out')
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context={
        'contacts': user_contacts
    }
    
    return render(request, 'accounts/dashboard.html', context)

