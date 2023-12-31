from django.urls import path,include
from . import views
       
urlpatterns=[
    path('',views.home,name='home'),
    path('get_latest_voltage/', views.get_latest_voltage),
    # path('login',include('django.contrib.auth.urls')  )
    path('logout/',views.userLogout,name='logout' ),
    path('register/',views.create_student,name='register'),
    path('login_student/',views.login_user,name='login_student'),
    path('student_dashboard/',views.student_dashboard,name='student_dashboard'),
    path('teacher_dashboard/',views.teacher_dashboard,name='teacher_dashboard'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('technical_team_dashboard/',views.technical_team_dashboard,name='technical_team_dashboard'),
]

