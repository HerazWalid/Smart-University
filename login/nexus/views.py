from django.shortcuts import render, redirect
import time 
from .anti_spoofing.test  import test 
from django.http import JsonResponse
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login ,logout
from django.shortcuts import render, redirect        
from django.contrib.auth.decorators import  login_required
from .decorators import notLoggedUsers , allowedUsers, forAdmins

def home(request):   
    return render(request,'AI/visitors_page/index.html')

#    ------------------------------------------ student dash board -----------------
@login_required(login_url='login_student')
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('login_student')
    return render(request,'AI/students/dashboard_students.html')
#    ------------------------------------------- teacher dashboard -----------------
@login_required(login_url='login_student')
def teacher_dashboard(request):
    if request.user.role != 'TEACHER':
        return redirect('login_student')
    return render(request,'AI/teachers/dashboard_teachers.html')
#    -------------------------------------------  admin dashbord ------------------
@login_required(login_url='login_student')
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        print('------------------------------------------------ reject')
        return redirect('login_student')
    return render(request,'AI/administration/dashboard_administration.html')
#    -------------------------------------------- techneical team dash board -------
@login_required(login_url='login_student')
def technical_team_dashboard(request):
    if request.user.role != 'TECHNICAL_TEAM':
        return redirect('login_student')
    return render(request,'AI/technical_team/dashboard_technecal_team.html')

def get_latest_voltage(request):
    try:
        # Query the latest VoltageData from the database
        latest_voltage_data = VoltageData.objects.latest('timestamp')
        
        # Extract the timestamp and voltage values
        timestamp = latest_voltage_data.timestamp
        voltage = latest_voltage_data.voltage
        
        # Return the data as JSON
        return JsonResponse({'timestamp': timestamp, 'voltage': voltage})
    except:
         print('will be returned -------')
         return JsonResponse({'timestamp': time.time(), 'voltage': 0.0})

# ---------------------- login --------------------

@notLoggedUsers
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'STUDENT':
            login(request, user)
            # Redirect to the appropriate student view after successful login
            return redirect('student_dashboard')  # Update with your student dashboard URL
        elif user is not None and user.role == 'ADMIN':
            login(request, user)
            # Redirect to the appropriate admin view after successful login
            return redirect('admin_dashboard')  # Update with your admin dashboard URL            
        elif user is not None and user.role == 'TEACHER':
            login(request, user)
            # Redirect to the appropriate teacher view after successful login
            return redirect('teacher_dashboard')  # Update with your teacher dashboard URL
        elif user is not None and user.role == 'TECHNICAL_TEAM':
            login(request, user)
            # Redirect to the appropriate teacher view after successful login
            return redirect('technical_team_dashboard')  # Update with your teacher dashboard URL
    return render(request, 'AI/user_registration/login_student.html')


# -------------------------------------------------- logout
def userLogout(request):  
    logout(request)
    return redirect('login_student') 



def create_student(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = StudentForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Create a new Student instance with the form data but don't save it yet
            new_student = form.save(commit=False)

            # You can perform additional processing or validation here if needed

            # Save the new student to the database
            new_student.save()

            # Optionally, you can redirect to a success page or another view
            return redirect('/index1')  # Replace 'success_page' with the actual URL name or path
    else:
        # If it's not a POST request, create a blank form
        form = StudentForm()

    # Render the HTML template with the form
    return render(request, 'AI/student_form.html', {'form': form})
     

     



