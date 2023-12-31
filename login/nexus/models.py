from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        STUDENT = "STUDENT", _("Student")
        TEACHER = "TEACHER", _("Teacher")
        TECHNICAL_TEAM = "TECHNICAL_TEAM", _("Technical Team")
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)

    # Add related_name to resolve clashes
    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="customuser_set",
        related_query_name="customuser",
    )

    def __str__(self):
        return f"{self.username} - {self.role}"

class VoltageData(models.Model):
    voltage = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)



class GroupL3(models.Model):
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name




class Student(models.Model):
    user=models.OneToOneField(CustomUser,null=True,on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20, default="0123456789")
    contact_phone = models.CharField(max_length=15, default="213-540-028-098")
    group_number = models.ForeignKey(GroupL3, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Teacher(models.Model):
    user=models.OneToOneField(CustomUser,null=True,on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20, default="0123456789")
    module = models.CharField(max_length=100,default='not_yet')
    contact_phone = models.CharField(max_length=15, default="213-540-028-098")
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Administration(models.Model):
    user=models.OneToOneField(CustomUser,null=True,on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20, default="0123456789")
    position = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15, default="213-540-028-098")
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class TechnicalTeam (models.Model):
    user=models.OneToOneField(CustomUser,null=True,on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20, default="0123456789")
    position = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15, default="213-540-028-098")
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class SetSession(models.Model):
    group = models.ForeignKey(GroupL3, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now) 
    class_name = models.CharField(max_length=50, choices=[('class_1', 'class_1'), ('class_2', 'class_2')])
    def __str__(self):
        return f'{self.time}'


class Attendance(models.Model):
    session = models.ForeignKey(SetSession, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'{self.session}'
