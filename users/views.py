from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .forms import *

def home(request):
    user = auth.get_user(request)
    if not user:
        messages.success(request, "Você precisa estar logado para acessar está página!")
        return redirect('login')
    
    user_data = CustomUser.objects.get(username=user.username)
    if not user_data:
        messages.success(request, "Usuário não encontrado.")
        return redirect('register')
    return render(request, 'users/home.html', {"user_data":user_data, "nec_data": { "count": user_data.transactions.all().count(), "alltrans": user_data.transactions.all()}})

def login(request):
    form = LoginForms()

    if request.method == "POST":
        form = LoginForms(request.POST)
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()

            user = auth.authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                auth.login(request, user)
                return redirect('home')
            messages.error(request, "usuário/senha estão incorretos ou usuário não existe!")
            return redirect('login')
    return render(request, 'users/login.html', {"form":form})

def register(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form['username'].value()
            email = form['email'].value()
            password_1 = form['password1'].value()

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Usuário já existe!")
                return render(request, 'users/register.html', {"form":form})
            
            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=password_1,
                wallet=0,
            )

            user.set_password(request.POST['password1'])
            user.save()

            return redirect('login')

    return render(request, 'users/register.html', {"form":form})

def logout(request):
    auth.logout(request)
    return redirect('index')

def deposit(request):
    form = DepositForm()

    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form['amount'].value()

            user = CustomUser.objects.get(username=request.user.username)
            user.wallet += float(amount)
            user.transactions.create(sender="Depósito", amount=amount)
            user.save()

            return redirect('home')

    return render(request, 'users/deposit.html', {"form":form})

def transfer(request):
    form = TransferForm()

    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = float(form['amount'].value())
            email = form['email'].value()

            user = CustomUser.objects.get(username=request.user.username)
            if user.email == email:
                messages.error(request, "Você não pode transferir para você mesmo.")
                return render(request, 'users/transfer.html', {"form":form})
            if user.wallet < amount:
                messages.error(request, "O Valor é maior que o saldo em conta.")
                return render(request, 'users/transfer.html', {"form":form})
            
            receiver = CustomUser.objects.get(email=email)
            if receiver is None:
                messages.error(request, "Este usuário não existe!")
                return render(request, 'users/transfer.html', {"form":form})
            
            user.wallet -= amount
            receiver.wallet += amount
            user.transactions.create(sender=f"{receiver.username}", amount=amount*-1)
            receiver.transactions.create(sender=f"{user.username}", amount=amount)
            user.save()
            receiver.save()

            return redirect('home')

    return render(request, 'users/transfer.html', {"form":form})