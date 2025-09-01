from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode

from vendor.forms import VendorForm

from .forms import UserForm
from .models import User
from .utils import check_role_customer, check_role_vendor, detect_user, send_email

# Create your views here.


def check_is_login(func):
    def wrapper(request):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in!")
            return redirect("my_account")
        return func(request)

    return wrapper


@check_is_login
def register_user(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password"))
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been register successfully")
            send_email(request, user, "send_verification_email")
            return redirect("login")
        else:
            messages.error(request, "Please fill valid details")
    else:
        form = UserForm()
    context = {"form": form}
    return render(request, "accounts/register_user.html", context)


@check_is_login
def register_vendor(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password"))
            user.role = User.RESTAURANT
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = user.profile
            vendor.save()
            messages.success(
                request,
                "Your account have been register successfully! Please wait for the approval.",
            )
            send_email(request, user, "send_verification_email")
            return redirect("login")
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {"form": form, "vendor_form": v_form}
    return render(request, "accounts/register_vendor.html", context)


@check_is_login
def login(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Please provide email and password")
            return redirect("login")
        user = authenticate(email=email, password=password)

        if not user:
            messages.error(request, "Invalid Login Credentials")
            return redirect("login")

        user_login(request, user)
        messages.success(request, "You are now logged in.")
        return redirect("my_account")

    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logout(request):
    user_logout(request)
    messages.info(request, "You are logged out")
    return redirect("login")


@login_required(login_url="login")
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    if not check_role_customer(request.user):
        return redirect("my_account")
    return render(request, "accounts/customer_dashboard.html")


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    return render(request, "accounts/vendor_dashboard.html")


@login_required(login_url="login")
def my_account(request):
    redirectUrl = detect_user(request.user)
    return redirect(redirectUrl)


def activate(request, uuid64, token):
    try:
        uid = urlsafe_base64_decode(uuid64).decode()
        user = User._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated!")
        return redirect("my_account")

    messages.error(request, "Invalid activation link")
    return redirect("my_account")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email__exact=email)
        if user.exists():
            send_email(request, user.first(), "send_reset_password_email")
            messages.success(
                request, "Reset password link is sent to your email successfully"
            )
            return redirect("forgot_password")
        messages.error(request, "Email does not exist")
        return redirect("forgot_password")

    return render(request, "accounts/forgot_password.html")


def reset_password_validate(request, uuid64, token):
    try:
        uid = urlsafe_base64_decode(uuid64).decode()
        user = User._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "Please reset your password")
        return redirect("reset_password")

    messages.error(request, "Invalid password reset link")
    return redirect("forgot_password")


def reset_password(request):
    uid = request.session.get("uid", None)
    if not uid:
        messages.error(request, "Invalid User")
        return redirect("forgot_password")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password == confirm_password:

            user = User.objects.get(id=uid)
            user.set_password(password)
            user.save()
            request.session.pop("uid", None)
            messages.success(request, "Password Reset Successfully")
            return redirect("login")
        else:
            messages.error(request, "Password not match")
            return redirect("reset_password")
    return render(request, "accounts/reset_password.html")
