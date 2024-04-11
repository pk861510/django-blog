from django.shortcuts import render,redirect
# from django.contrib.auth.forms import UserCreationForm no need bcz we create a form.py and import from there
from django.contrib import messages
from.forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method =="POST":
        form = UserRegisterForm(request.POST)  # form contain data from post request username and two password fieldsand we also added two filds email and custom_fiels in this
        if form.is_valid():  #Django backend check if we want to save user then simply add line form.save()
            form.save()
            username = form.cleaned_data.get('username')# This will create a dictionary
            messages.success(request,f'Smile please! Your account has been created! You are now able to log in.')
            return redirect('Login')

    else:
        form = UserRegisterForm()

    return render(request,'users/register.html',{'form':form})


@login_required()
def profile(request):

    u_form = UserUpdateForm(request.POST,instance=request.user)
    p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, f'Smile please! Your account has been Updated!.')
        return redirect('Profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
                'u_form':u_form,
                'p_form':p_form
               }
    return render(request,'users/profile.html',context)

