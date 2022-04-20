from unicodedata import name
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from account.models import TransactionHistory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from account.forms import SignupForm, AddRemoveBalanceForm
from account.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.serializers import CheckBalanceSerializer, RegisterUserSerializer, UpdateBalanceSerializer
from django.contrib import messages
from django.core.paginator import Paginator


def home_page(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        form = AddRemoveBalanceForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            ubalance = form.cleaned_data['balance']
            if ubalance > 0.00:
                if request.POST.get('add'):
                    user.balance += ubalance
                    messages.success(request, 'Amount deposited successfully')

                if request.POST.get('remove'):
                    user.balance -= ubalance
                    messages.success(request, 'Amount widthdraw successfully')
                TransactionHistory(user=request.user, transaction_amount=ubalance, added_by=request.user).save()
            else:
                messages.error(request, 'Enter amount greater then 0')
            user.save()

        form = AddRemoveBalanceForm()
        histories = TransactionHistory.objects.filter(user=user_id).order_by('-id')

        histories_paginator = Paginator(histories, 5)
        page_num = request.GET.get('page')
        transaction = histories_paginator.get_page(page_num)
        totalpages = transaction.paginator.num_pages

        context = {'transactions': transaction, 'user': user, 'form': form,'lastpage':totalpages, 'totalpagecount':[n+1 for n in range(totalpages)]}
        return render(request, 'py_wallet/dashboard.html', context)
    else:
        messages.error(request, 'Please Login.')
        return HttpResponseRedirect('/login')


def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            register_user = User.objects.create(email = email, password = password)
            register_user.save()
            messages.success(request, 'Profile Created Successfully.')
            return redirect('/login')
    form = SignupForm()
    return render(request, 'py_wallet/signup.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uemail = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(email=uemail, password=upass)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
    form = AuthenticationForm()
    return render(request, 'py_wallet/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@api_view(['POST'])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'status': 403, 'error': serializer.errors, 'message': 'Something went wrong'})
    serializer.save()

    return Response({'status': 200, 'payload': serializer.data, 'message': 'Your data is saved'})


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def balance_check(request):
    serializer = CheckBalanceSerializer(request.user)
    return Response(serializer.data)


@api_view(['PATCH'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def balance_update(request):
    try:
        update_balance = User.objects.get(id=request.user.id)
        serializer = UpdateBalanceSerializer(
            update_balance, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(status=400, data={
                'status': 400, 'error': serializer.errors, 'message': 'Validation errors.'})
        serializer.save()

        return Response({'status': 200, 'payload': serializer.data, 'message': 'Your data is saved'})

    except Exception as e:
        return Response({'status': 400, 'message': 'Bad Request'})
