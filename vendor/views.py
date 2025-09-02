from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accoounts.forms import UserProfileForm
from accoounts.models import UserProfile

from .forms import VendorForm
from .models import Vendor

# Create your views here.


def v_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user_profile=profile)
    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)

    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Your restuarant details updated successfully")
            return redirect("v_profile")
        else:
            print("Error")
            print(profile_form.errors)
            print(vendor_form.errors)

    context = {"profile_form": profile_form, "vendor_form": vendor_form}
    return render(request, "vendor/v_profile.html", context)
