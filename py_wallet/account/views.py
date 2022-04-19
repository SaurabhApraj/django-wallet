from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from account.models import TransactionHistory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from account.forms import SignupForm, AddRemoveBalanceForm
from account.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.serializers import CheckBalanceSerializer, RegisterUserSerializer, UpdateBalanceSerializer


def homePage(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        form = AddRemoveBalanceForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            ubalance = form.cleaned_data['balance']
            if ubalance > 0.00:
                user.balance += ubalance
            # user.balance -= ubalance
            else:
                return HttpResponse('Amount should be greater then 0')
            TransactionHistory(
                user=request.user, transaction_amount=ubalance, added_by=request.user).save()
            user.save()
        form = AddRemoveBalanceForm()
        histories = TransactionHistory.objects.filter(
            user=user_id).order_by('-id')
        context = {'histories': histories, 'user': user, 'form': form}
        return render(request, 'py_wallet/dashboard.html', context)
    else:
        return HttpResponseRedirect('/login')


def userSignup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            em = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            reg = User(email=em, password=pw)
            reg.save()
            return redirect('/login')
    form = SignupForm()
    return render(request, 'py_wallet/signup.html', {'form': form})


def userlogin(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            # uemail = fm.cleaned_data.get('email', None)
            uemail = fm.cleaned_data['email']
            upass = fm.cleaned_data['password']
            user = authenticate(email=uemail, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('')
    fm = AuthenticationForm()
    return render(request, 'py_wallet/login.html', {'form': fm})


def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@api_view(['POST'])
def registerUser(request):
    serializer = RegisterUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'status': 403, 'error': serializer.errors, 'message': 'Something went wrong'})
    serializer.save()

    return Response({'status': 200, 'payload': serializer.data, 'message': 'Your data is saved'})


@api_view(['GET'])
def checkBalance(request):
    check_balance = User.objects.get(id=request.user.id)
    serializer = CheckBalanceSerializer(check_balance)
    return Response(serializer.data)


@api_view(['PATCH'])
def updateBalance(request):
    try:
        update_balance = User.objects.get(id=request.user.id)
        serializer = UpdateBalanceSerializer(
            update_balance, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response({
                'status': 403, 'error': serializer.errors, 'message': 'Something went wrong'})
        serializer.save()

        return Response({'status': 200, 'payload': serializer.data, 'message': 'Your data is saved'})

    except Exception as e:
        return Response({'status': 403, 'message': 'invalid id'})


# class BalanceAPI(APIView):
#     def get(self,request):
#         check_balance = User.objects.all()
#         serializer = CheckBalanceSerializer(check_balance, many=True)
#         return Response(serializer.data)

#     def patch(self, request):
#         try:
#             update_balance = User.objects.get(id=id)
#             serializer = UpdateBalanceSerializer(
#                 update_balance, data=request.data, partial=True)

#             if not serializer.is_valid():
#                 return Response({
#                     'status': 403, 'error': serializer.errors, 'message': 'Something went wrong'})
#             serializer.save()

#             return Response({'status': 200, 'payload': serializer.data, 'message': 'Your data is saved'})

#         except Exception as e:
#             return Response({'status': 403, 'message': 'invalid id'})
