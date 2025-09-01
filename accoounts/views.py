from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserForm
from .models import User

from vendor.forms import VendorForm
from vendor.models import Vendor


# Create your views here.

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been register successfully')
            return redirect('register_user')
        else:
            print(form.errors)
            messages.error(request, 'Please fill valid details')
    else:  
        form = UserForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/register_user.html', context)

def register_vendor(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.role = User.RESTAURANT
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = user.profile
            vendor.save()
            messages.success(request, 'Your account have been register successfully! Please wait for the approval.')
            return redirect('register_vendor')

    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form' : form,
        'vendor_form' : v_form
    }
    return render(request, 'accounts/register_vendor.html', context)
    