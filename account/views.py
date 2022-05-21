from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .models import Customer,Verification
from .send_sms import send_sms

def log_in(request):
    if request.method == 'POST':
        phone_number=request.POST.get('phone_number',None)
        password = request.POST.get('password', None)
        cutomer=authenticate(phone_number=phone_number,password=password)
        print(cutomer)
        if cutomer:
            login(request,cutomer)
            return redirect('home')
    return render(
        request=request,
        template_name='auth/signin.html'
    )

def password_reset(request):
    code_message:str=''
    password_message:str=''
    if request.method == 'POST':
        code=request.POST.get('code',None)
        password = request.POST.get('password', None)
        password1 = request.POST.get('password1', None)
        verification = Verification.objects.get(code=code)
        print(verification.user)
        if verification:
            if password == password1:
                verification.user.set_password(password)
                verification.user.save()
                return redirect('login')
            else:
                password_message = 'Please make sure password fields is same !'
        else:
            code_message = 'Given code error!'
    return render(
        request=request,
        template_name='auth/password_reset.html',
        context={
            'code_message':code_message,
            'password_message':password_message
        }
    )

def password_phone(request):
    if request.method == 'POST':
        phone_number:str=request.POST.get('phone_number',None)
        user=Customer.objects.get(phone_number=phone_number)
        verification = Verification.code_generate(user)
        send_sms(phone_number, f'{verification.code}\nBu sizning tasdiqlash kodingiz. Uni hech kimga bermang!')
        if phone_number:
            return redirect('password_reset')
        else:
            return redirect('password_phone')
    return render(
        request=request,
        template_name='auth/password_phone.html'
    )


def verification(request):
    if request.method == 'POST':
        code=request.POST.get('code',None)
        try:
            if code:
                verification=Verification.objects.get(code=code)
                user=verification.user
                user.is_verified=True
                user.save()
                return redirect('home')
            else:
                ValueError
        except:
            pass
    return render(
        request=request,
        template_name='auth/verification.html'
    )

def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def register(request):
    print(request.POST)
    user_message:str=''
    password_message:str=''
    if request.method=='POST':
        first_name=request.POST.get('first_name',None)
        last_name = request.POST.get('last_name', None)
        phone_number = request.POST.get('phone_number', None)
        gender=request.POST.get('gender',None)
        password = request.POST.get('password', None)
        password1 = request.POST.get('password1', None)
        user=Customer.objects.filter(phone_number=phone_number)
        if user:
             user_message='This phone number is busy!'
        elif password1 !=password:
            password_message='Please make sure password fields is same !'
        else:
            user = Customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                gender=gender,
                password=password
            )
            user.set_password(password)
            user.save()
            verification=Verification.code_generate(user)
            send_sms(user.phone_number,f'{verification.code}\nBu sizning tasdiqlash kodingiz. Uni hech kimga bermang!')
            login(request,user)
            return redirect('verification')
    return render(
        request=request,
        template_name='auth/signup.html',
        context={
            'user_message':user_message,
            'password_message':password_message
        }
    )

