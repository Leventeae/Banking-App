from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, BankAccountForm
from .models import BankAccount
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.contrib import messages
from django.http import HttpResponse
import random
import csv

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect authenticated users to the dashboard
    return render(request, 'home.html')

def profile(request):
    return render(request, 'accounts/profile.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            return HttpResponse("Invalid credentials", status=401)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)  # This will log the user out
    return redirect('login')

# Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Account creation view
@login_required
def create_account(request):
    if request.method == 'POST':
        # Generate a random bank account number (e.g., 10-digit random number)
        account_number = random.randint(1000000000, 9999999999)

        # Create the new bank account
        new_account = BankAccount(user=request.user, account_number=account_number)
        new_account.save()

        return redirect('dashboard')
    return render(request, 'accounts/create_account.html')

# Dashboard view
@login_required
def dashboard(request):
    # Get the current user's bank accounts
    bank_accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'accounts/dashboard.html', {'bank_accounts': bank_accounts})

# Deposit view
@login_required
def deposit(request, account_id):
    account = BankAccount.objects.get(id=account_id)

    if request.method == 'POST':
        deposit_amount = request.POST.get('amount')
        
        try:
            deposit_amount = Decimal(deposit_amount)  # Convert amount to Decimal
            if deposit_amount <= 0:
                messages.warning(request, "Deposit amount must be greater than zero.")
                return redirect('deposit', account_id=account_id)
        except (InvalidOperation, ValueError):
            messages.warning(request, "Invalid deposit amount.")
            return redirect('deposit', account_id=account_id)

        account.balance += deposit_amount  # Add the deposit to the balance
        account.save()
        messages.success(request, "Deposit successful.")
        return redirect('dashboard')  # Redirect to the dashboard after deposit

    return render(request, 'accounts/deposit.html', {'account': account})

# Withdraw view
@login_required
def withdraw(request, account_id):
    account = BankAccount.objects.get(id=account_id)

    if request.method == 'POST':
        withdraw_amount = request.POST.get('amount')
        
        try:
            withdraw_amount = Decimal(withdraw_amount)  # Convert amount to Decimal
            if withdraw_amount <= 0:
                messages.warning(request, "Withdrawal amount must be greater than zero.")
                return redirect('withdraw', account_id=account_id)
        except (InvalidOperation, ValueError):
            messages.warning(request, "Invalid withdrawal amount.")
            return redirect('withdraw', account_id=account_id)

        if withdraw_amount > account.balance:
            messages.warning(request, "Insufficient funds.")
            return redirect('withdraw', account_id=account_id)

        account.balance -= withdraw_amount  # Subtract the withdrawal amount from the balance
        account.save()
        messages.success(request, "Withdrawal successful.")
        return redirect('dashboard')  # Redirect to the dashboard after withdrawal

    return render(request, 'accounts/withdraw.html', {'account': account})

def download_all_accounts_data(request):
    # Retrieve all accounts for the logged-in user
    accounts = BankAccount.objects.filter(user=request.user)
    
    # Set up the CSV response with a filename based on the user's name
    filename = f"{request.user}_accounts_data.csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Initialize the CSV writer
    writer = csv.writer(response)

    # Write the header row - adjust fields based on your model
    writer.writerow(['Account Number', ' Balance'])

    # Write each account's data as a row in the CSV
    for account in accounts:
        writer.writerow([account.account_number, ' $' + str(account.balance)])

    return response