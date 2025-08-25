from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from .models import User

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
    else:  
        form = UserForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/register_user.html', context)