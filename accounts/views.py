from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
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
            mail_subject = 'Please activate Your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            to_mail = email
            send_mail = EmailMessage(
                mail_subject,
                message,
                to=[to_mail]
            )
            send_mail.send()
            # messages.success(request, 'Your account was created successfully')
            return redirect('/login/?command=verification&email=' + email)
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
                    return redirect('login')
            else:
                messages.error(request, 'that account does not exists')
                return redirect('login')
        else:
            messages.error(request, 'invalid email or password')
            return redirect('login')

    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'You have confirmed your account go ahead and login!')
        return redirect('login')
    else:
        messages.error(request, 'link is expired!')
        return redirect('signup')



# Request Password Reset View
def password_reset(request):
    if request.method == 'POST':
        # Here we're using html form input to get the email, but we can use django forms to make form inputs dynamic.
        # So, use django forms to make email form instead.
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Please activate Your account'
            message = render_to_string('accounts/password_reset_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            to_mail = email
            send_mail = EmailMessage(
                mail_subject,
                message,
                to=[to_mail]
            )
            send_mail.send()
            messages.success(request, 'We have sent password reset email to your email address')
            return redirect('login')
        else:
            messages.error(request, 'account does not exits, please try again!')
            return redirect('password_reset')
    return render(request, 'accounts/password_reset.html')

def password_reset_done(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset your password')
        return redirect('password_reset_confirm')
    else:
        messages.error(request, 'the link has been expired')
        return redirect('password_reset')

def password_reset_confirm(request):
    if request.method == 'POST':
        # Here we're using html form inputs to get password and password confirm, but we can use django forms to make form inputs dynamic.
        # So, use django forms to make password and password confirm form instead.
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        if password_confirm == password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been set. go ahead and login')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('password_reset_confirm')
    else:
        return render(request, 'accounts/password_reset_confirm.html')