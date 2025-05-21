from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, CustomAuthenticationForm
from .models import User
import random
import string

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('login')

@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('barangay_dashboard')

def password_reset1(request):
    """
    First step of password reset - email form
    """
    return render(request, 'accounts/password_reset1.html')

def password_reset_confirm(request):
    """
    Process the email form and send recovery code
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if email exists in the database
        try:
            user = User.objects.get(email=email)
            
            # Generate a random 6-digit code
            recovery_code = ''.join(random.choices(string.digits, k=6))
            
            # Store in session
            request.session['recovery_email'] = email
            request.session['recovery_code'] = recovery_code
            
            # In a real app, you would send an email here with the code
            messages.success(request, f"Recovery code sent to {email}. For testing purposes, the code is: {recovery_code}")
            
            # Redirect to the password reset page where they enter the code
            return redirect('password_reset')
        except User.DoesNotExist:
            return render(request, 'accounts/password_reset1.html', {'error_message': 'Email not found in our records.'})
    
    return redirect('password_reset1')

def password_reset(request):
    """
    Second step of password reset - enter code and new password
    """
    if 'recovery_email' not in request.session:
        return redirect('password_reset1')
        
    if request.method == 'POST':
        recovery_code = request.POST.get('recovery_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        stored_code = request.session.get('recovery_code')
        email = request.session.get('recovery_email')
        
        # Validate the code and passwords
        if recovery_code != stored_code:
            return render(request, 'accounts/password_reset.html', {'error_message': 'Invalid recovery code.'})
        
        if new_password != confirm_password:
            return render(request, 'accounts/password_reset.html', {'error_message': 'Passwords do not match.'})
        
        # Update the password
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            # Clear session data
            del request.session['recovery_email']
            del request.session['recovery_code']
            
            messages.success(request, 'Password has been reset successfully. You can now log in with your new password.')
            return redirect('login')
        except User.DoesNotExist:
            return render(request, 'accounts/password_reset.html', {'error_message': 'User not found.'})
    
    return render(request, 'accounts/password_reset.html')