from django.shortcuts import render
import random
from django.utils import timezone
from datetime import timedelta
from .forms import CreateUserForm, LoginForm, EmailVerificationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import EmailVerification
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorReading, EmailVerification
from django.db import models
import json







def home(request):
    
    return render(request, 'home.html')



def register(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            try:
                user=form.save(commit=False)
                user.is_active=False
                user.save()
                code=str(random.randint(100000, 999999))
                EmailVerification.objects.create(user=user, code=code)
                
                # Send email (will print to console in development)
                send_mail(
                    'IoT Monitor - Email Verification Code',
                    f'Your Verification Code is: {code}\n\nThis code expires in 15 minutes.\n\nIf you did not request this code, please ignore this email.',
                    'noreply@iotmonitor.com',  # Professional sender email
                    [user.email],
                    fail_silently=False,
                )
                
                request.session['pending_user_id']=user.id
                print(f"Registration successful for user {user.username}, code: {code}")  # Debug
                return redirect('Verify_email')
                
            except Exception as e:
                print(f"Registration error: {e}")  # Debug
                form.add_error(None, f'Registration failed: {str(e)}')
        
    return render(request, 'register.html', {'form':form})


def Verify_email(request):
    form=EmailVerificationForm()
    user_id=request.session.get('pending_user_id')
    print(f"Verify_email view called, user_id: {user_id}")  # Debug
    
    if not user_id:
         print("No pending user ID, redirecting to register")  # Debug
         return redirect('register')
    
    try:
        user=User.objects.get(id=user_id)
        print(f"Found user: {user.username}")  # Debug
    except User.DoesNotExist:
        print("User not found, redirecting to register")  # Debug
        return redirect('register')
    
    if request.method=='POST':
        form=EmailVerificationForm(request.POST)
        if form.is_valid():
            code=form.cleaned_data['code']
            try:
                 expiry_window=timezone.now()-timedelta(minutes=15)
                 verification=EmailVerification.objects.get(user=user, code=code, is_used=False, created_at__gte=expiry_window)
                 user.is_active=True
                 user.save()
                 verification.is_used=True
                 verification.save()
                 del request.session['pending_user_id']
                 print(f"Email verification successful for {user.username}")  # Debug
                 return redirect('login')
            except EmailVerification.DoesNotExist:
                 print(f"Invalid verification code: {code}")  # Debug
                 form.add_error('code', 'Invalid Verification Code')                 
    return render (request, 'verify_email.html', {'form':form})


def login(request):
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(request, data=request.POST)
        if form.is_valid():
            username=form.POST.get('username')
            password=form.POST.get('password')
            user=authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
    context={'form':form}

    return render(request, 'login.html', context=context)
                 
    

def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    # Get the latest sensor readings
    latest_reading = SensorReading.objects.first()  # Most recent reading
    
    # Get readings for the last 24 hours for charts
    from datetime import datetime, timedelta
    yesterday = timezone.now() - timedelta(days=1)
    recent_readings = SensorReading.objects.filter(timestamp__gte=yesterday).order_by('timestamp')
    
    # Calculate statistics
    total_readings = SensorReading.objects.count()
    
    # Get average values
    avg_temp = SensorReading.objects.aggregate(avg_temp=models.Avg('temprature'))['avg_temp']
    avg_humidity = SensorReading.objects.aggregate(avg_humidity=models.Avg('humidity'))['avg_humidity']
    
    context = {
        'latest_reading': latest_reading,
        'recent_readings': recent_readings,
        'total_readings': total_readings,
        'avg_temp': round(avg_temp, 1) if avg_temp else 0,
        'avg_humidity': round(avg_humidity, 1) if avg_humidity else 0,
    }
    
    return render(request, 'dashboard.html', context)

@csrf_exempt
def recieve(request):
    if request.method=="POST":
        
        try:
            data=json.loads(request.body)
            temp=data.get('temprature')
            humid=data.get('humidity')
            if temp is not None and humid is not None:
                SensorReading.objects.create(temprature=temp, humidity=humid)
                return JsonResponse({'status': 'success', 'message': 'data_saved'}, status=201)
            else:
                return JsonResponse({'status':'error', 'message':'Missing data fields'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status':"error", 'message':'Invalid JSON format'}, status=400)
        except Exception as e:
            print(f" Error saving data : {e}" )
            return JsonResponse({'status':'error', 'message': str(e)}, status=500)
    return JsonResponse({"status": "info", "message": "Send data via POST"}, status=200)
        






# Create your views here.
