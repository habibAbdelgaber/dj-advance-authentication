from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from .forms import UserRegistrationForm, LoginForm

from django.contrib import auth
from django.contrib.auth import authenticate


# Account Verification
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            # phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            user = Account.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            # user.phone_number = phone_number
            user.save()
            current_site = get_current_site(request)
            mail_object = 'Please activate Your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            to_mail = email
            send_mail = EmailMessage(
                mail_object,
                message,
                to=[to_mail]
            )
            send_mail.send()
            # messages.success(request, 'Your account was created successfully')
            return redirect('/signin/?command=verification&email=' + email)
        # else:
        #     messages.error(request, 'Something went wrong, please try again')
        #     return redirect('signup')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def signout(request):
    auth.logout(request)
    messages.success(request, 'You have logged out')
    return redirect('/')

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'You have logged in successfully!')
                    return redirect('/')
                else:
                    messages.error(request, 'Please confirm or activate you account and login')
                    return redirect('signin')
            else:
                messages.error(request, 'that account does not exists')
                return redirect('signin')
        else:
            messages.error(request, 'invalid email or password')
            return redirect('signin')

    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)

def activate(request, uidb64, token):
    return HttpResponse('ok')    