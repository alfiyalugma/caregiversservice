from django.db import models
from datetime import datetime

class MyUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    given_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    city = models.CharField(null=True, max_length=100)
    phone_number = models.CharField(max_length=15)
    profile_description = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.given_name

class Caregiver(models.Model):
    caregiver_user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    photo = models.ImageField(null=True, upload_to='profile_images', default='blank_profile_image.jpg')
    gender = models.CharField(max_length=10)
    caregiving_type = models.CharField(max_length=50)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

class Member(models.Model):
    member_user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    house_rules = models.TextField(null=True)

class Address(models.Model):
    member_user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    house_number = models.CharField(max_length=10)
    street = models.CharField(max_length=100)
    town = models.CharField(max_length=100)

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    member_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    required_caregiving_type = models.CharField(max_length=50)
    other_requirements = models.TextField()
    date_posted = models.DateField(default=datetime.now)

class Job_Application(models.Model):
    caregiver_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date_applied = models.DateField(default=datetime.now)

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    caregiver_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='appointments_as_caregiver')
    member_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='appointments_as_member')
    appointment_date = models.DateField(default=datetime.now)
    appointment_time = models.TimeField(default=datetime.now)
    work_hours = models.IntegerField()
    status = models.CharField(max_length=20)
