from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from account.forms import CreateUserForm, LoginForm, UpdateUserForm
from account.token import user_token_generator
from payment.forms import ShippingForm
from payment.models import ShippingAddress


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            # Email verification setup(template)
            current_site = get_current_site(request)
            subject = 'Account verification email'
            message = render_to_string('account/registration/email-verification.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_token_generator.make_token(user)
            })

            user.email_user(subject=subject, message=message)

            return redirect('account:email-verification-sent')
    context = {'form': form}
    return render(request, 'account/registration/register.html', context)


def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('account:dashboard')
    context = {'form': form}
    return render(request, 'account/my-login.html', context)


def user_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
    messages.success(request, 'Logout success')
    return redirect('store:store')


@login_required(login_url='account:my-login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


def email_verification(request, uid64, token):
    #unique token
    unique_id = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=unique_id)

    # Success
    if user and user_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('account:email-verification-success')
    # Failed
    else:
        return redirect('account:email-verification-failed')


def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')


def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')


def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')


@login_required(login_url='account:my-login')
def profile_management(request):
    # Update profile

    user_form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.info(request, 'Account updated')
            return redirect('account:dashboard')


    context = {'user_form': user_form}
    return render(request, 'account/profile-management.html', context)


@login_required(login_url='account:my-login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        messages.error(request, 'Account deleted successfully')
        return redirect('store:store')
    return render(request, 'account/delete-account.html')


@login_required(login_url='account:my-login')
def manage_shipping(request):
    try:
        shipping = ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
        shipping = None
    form = ShippingForm(instance=shipping)
    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            shipping_user = form.save(commit=False)
            shipping_user.user = request.user
            shipping_user.save()
            return redirect('account:dashboard')

    context = {'form': form}
    return render(request, 'account/manage-shipping.html', context)


def check_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    return JsonResponse({}, status=400)











