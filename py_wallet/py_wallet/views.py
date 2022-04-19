from django.shortcuts import render
from django.http import HttpResponseRedirect
from account.models import TransactionHistory, User

def homePage(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.filter(id = user_id)
        histories = TransactionHistory.objects.filter(user = user)
        return render(request, 'account/dashboard.html',{'histories':histories})
    else:
        return HttpResponseRedirect('/login')