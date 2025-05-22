from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from buyer.forms import BuyersForm


# Create your views here.
def signin(request):
    if request.method == 'POST':
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=useremail, password=password)
        if user is not None:
            login(request, user=user)
            print("Da")
        else:
            print(request.user.password)
            print("Hi")


    buyersForm = BuyersForm
    return render(request, 'buyer/login.html',{'buyersForm':buyersForm})

def signup(request):
    error = ''
    if request.method == 'POST':
        form = BuyersForm(request.POST)
        if form.is_valid():
            buyer = form.save(commit=False)  # ❗ НЕ сохраняем сразу
            buyer.set_password(form.cleaned_data['password'])  # 🔐 Хэшируем
            buyer.save()  # ✅ Теперь сохраняем
        else:
            error = 'Ошибка'

    buyersForm = BuyersForm
    return render(request, 'buyer/signup.html',{'buyersForm':buyersForm})