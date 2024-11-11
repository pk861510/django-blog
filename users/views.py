from django.shortcuts import render,redirect
# from django.contrib.auth.forms import UserCreationForm no need bcz we create a form.py and import from there
from django.contrib import messages
from.forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth import get_user_model

import base64
from io import BytesIO
import pyotp
import qrcode

# Create your views here.
User = get_user_model()


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




def verify_2fa(request):
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('login')
    
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        code = request.POST.get('code')
        totp = pyotp.TOTP(user.profile.mfa_secret)

        # Use a valid window of 1 to allow a slight time drift
        if totp.verify(code, valid_window=1):
            login(request, user)
            del request.session['pre_2fa_user_id']
            messages.success(request, "Login successful with 2FA.")
            return redirect('Blog-home')
        else:
            messages.error(request, "Invalid 2FA code. Please try again.")

    return render(request, 'users/verify_2fa.html')

@login_required
def profile(request):
    u_form = UserUpdateForm(request.POST or None, instance=request.user)
    p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    
    profile_instance = request.user.profile

    # Generate QR code if 2FA is enabled
    qr_code_image = None
    if profile_instance.mfa_enabled and profile_instance.mfa_secret:
        totp = pyotp.TOTP(profile_instance.mfa_secret)
        qr_code_url = totp.provisioning_uri(name=request.user.username, issuer_name="YourAppName")

        # Generate QR Code image as base64
        qr = qrcode.make(qr_code_url)
        buffered = BytesIO()
        qr.save(buffered, format="PNG")
        qr_code_image = base64.b64encode(buffered.getvalue()).decode()

    if request.method == 'POST':
        # Check if 2FA enable/disable button was clicked
        if 'enable_2fa' in request.POST and not profile_instance.mfa_enabled:
            profile_instance.mfa_enabled = True
            profile_instance.mfa_secret = pyotp.random_base32()  # Generate new secret for 2FA
            profile_instance.save()
            messages.success(request, "2FA enabled! Use the QR code to set it up.")
            return redirect('Profile')

        elif 'disable_2fa' in request.POST and profile_instance.mfa_enabled:
            profile_instance.mfa_enabled = False
            profile_instance.mfa_secret = ''  # Clear MFA secret
            profile_instance.save()
            messages.success(request, "2FA has been disabled.")
            return redirect('Profile')

        # Otherwise, handle profile update form submission
        elif u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('Profile')

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'qr_code_image': qr_code_image,  # Pass the QR code URL to the template
        'mfa_enabled': profile_instance.mfa_enabled,
    }
    return render(request, 'users/profile.html', context)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # Use the existing login template

    def form_valid(self, form):
        user = form.get_user()
        
        # Check if user has 2FA enabled
        if user.profile.mfa_enabled:
            # Redirect to 2FA verification page
            self.request.session['pre_2fa_user_id'] = user.id
            return redirect('verify_2fa')

        # Otherwise, log the user in directly
        login(self.request, user)
        messages.success(self.request, f'Welcome back, {user.username}!')
        return redirect('Blog-home')  # or another page of your choice

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

