from django.shortcuts import render, redirect
from .models import MyUser, Member, Caregiver, Address, Job, Job_Application, Appointment
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests

@login_required(login_url='login')
def index(request):
    return redirect('profilepage')

def registration(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        given_name = request.POST['given_name']
        surname = request.POST['surname']
        phone_number = request.POST['phone_number']
        profile_description = request.POST['profile_description']

        if password == password2:
            if MyUser.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('registration')
            elif len(password) < 8:
                messages.info(request, 'Password must be at least 8 characters long')
                return redirect('registration')
            else:
                myuser = MyUser.objects.create(email=email, given_name=given_name, surname=surname, phone_number=phone_number, profile_description=profile_description, password=password)
                myuser.save()
                user = User.objects.create(username=email, email=email, password=password)
                user.save()

                auth.login(request, user)

                if profile_description == 'Member':
                    return redirect('registration_member')
                elif profile_description == 'Caregiver':
                    return redirect('registration_caregiver')
        else:
            messages.info(request, 'Password dismatch')
            return redirect('registration')
    else:
        return render(request, 'main/registration.html')

@login_required(login_url='login')
def registration_member(request):
    if request.method == 'POST':
        city = request.POST['city']
        town = request.POST['town']
        street = request.POST['street']
        house_number = request.POST['house_number']
        house_rules = request.POST['house_rules']
        myuser_instance = MyUser.objects.get(email=request.user)
        myuser_instance.city = city

        member_instance = Member.objects.create(member_user=myuser_instance)
        member_instance.house_rules = house_rules

        address_instance = Address.objects.create(member_user=myuser_instance)
        address_instance.town = town
        address_instance.street = street
        address_instance.house_number = house_number

        myuser_instance.save()
        member_instance.save()
        address_instance.save()

        return redirect('profilepage')
    else:
        return render(request, 'main/registration_member.html')

@login_required(login_url='login')
def registration_caregiver(request):
    if request.method == 'POST':
        city = request.POST['city']
        hourly_rate = request.POST['hourly_rate']
        gender = request.POST['gender']
        caregiving_type = request.POST['caregiving_type']

        myuser_instance = MyUser.objects.get(email=request.user)
        myuser_instance.city = city

        caregiver_instance = Caregiver.objects.create(
            caregiver_user=myuser_instance,
            hourly_rate=hourly_rate,
            gender=gender,
            caregiving_type=caregiving_type
        )

        if 'image' in request.FILES:
            image = request.FILES['image']
            caregiver_instance.photo = image

        myuser_instance.save()
        caregiver_instance.save()

        return redirect('profilepage')
    else:
        return render(request, 'main/registration_caregiver.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if email is not None:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.info(request, 'User with this email does not exist')
                return redirect('login')
            if user.password == password:
                auth.login(request, user)
                return redirect('profilepage')
            else:
                messages.info(request, 'Invalid login')
                return redirect('login')
        else:
            messages.info(request, 'Please enter your login credentials')
            return redirect('login')
    else:
        return render(request, 'main/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def profilepage(request, email=None):
    if str(request.user) == str(email):
        email = None
    if email:
        profile = MyUser.objects.get(email=email)
        other_user = True
    else:
        profile = MyUser.objects.get(email=request.user)
        other_user = None
    if profile.profile_description == "Member":
        member_instance = Member.objects.get(member_user=profile)
        address_instance = Address.objects.get(member_user=profile)
        job_instance = Job.objects.filter(member_user=profile)
    elif profile.profile_description == "Caregiver":
        caregiver_instance = Caregiver.objects.get(caregiver_user=profile)
    logged_user = MyUser.objects.get(email=request.user)
    if logged_user.profile_description == 'Member' and profile.profile_description == "Caregiver":
        job_instance = Job.objects.filter(member_user=logged_user)
    context = {
        'profile': profile,
        'other_user': other_user,
        'logged_user': logged_user,
        'logged_user_id': logged_user.user_id,
        'member': member_instance if profile.profile_description == "Member" else None,
        'address': address_instance if profile.profile_description == "Member" else None,
        'listed_jobs': job_instance if profile.profile_description == "Member" else None,
        'hiring_jobs': job_instance if logged_user.profile_description == 'Member' else None,
        'caregiver': caregiver_instance if profile.profile_description == "Caregiver" else None,
    }
    if request.method == 'POST':
        if 'caregiver_apply' in request.POST:
            applied_caregiver = request.POST['applied_caregiver']
            applied_job = request.POST['applied_job']
            applied_caregiver_instance = MyUser.objects.get(user_id=applied_caregiver)
            applied_job_instance = Job.objects.get(job_id=applied_job)
            job_application = Job_Application.objects.create(caregiver_user=applied_caregiver_instance, job=applied_job_instance)
            job_application.save()
            return render(request, 'main/application_created.html')
        if 'member_apply' in request.POST:
            applied_caregiver = request.POST['applied_caregiver']
            applied_job = request.POST['applied_job']
            applied_caregiver_instance = MyUser.objects.get(user_id=applied_caregiver)
            applied_job_instance = Job.objects.get(job_id=applied_job)
            job_application = Job_Application.objects.create(caregiver_user=applied_caregiver_instance, job=applied_job_instance)
            job_application.save()
            return render(request, 'main/application_created.html')
        if 'delete_job' in request.POST:
            job = request.POST['job']
            job_delete = Job.objects.get(job_id=job)
            job_delete.delete()
    return render(request, 'main/profilepage.html', context)

@login_required(login_url='login')
def network(request):
    logged_user = MyUser.objects.get(email=request.user)
    logged_user_description = logged_user.profile_description
    if request.method == 'POST':
        searched_type = request.POST['searched_type']
        if logged_user_description == 'Member':
            searched_users = Caregiver.objects.filter(caregiving_type=searched_type)
        elif logged_user_description == 'Caregiver':
            searched_users = Job.objects.filter(required_caregiving_type=searched_type)
        context = {
            'is_post_request': True,
            'logged_user': logged_user,
            'users': searched_users,
        }
        return render(request, 'main/network.html', context)
    else:
        return render(request, 'main/network.html', {'is_post_request': False})

@login_required(login_url='login')
def create_application(request):
    if request.method == 'POST':
        required_caregiving_type = request.POST['required_caregiving_type']
        other_requirements = request.POST['other_requirements']

        current_member = MyUser.objects.get(email=request.user)
        new_job = Job.objects.create(member_user=current_member, required_caregiving_type=required_caregiving_type, other_requirements=other_requirements)
        new_job.save()

        return render(request, 'main/application_created.html')
    else:
        return render(request, 'main/create_application.html')

@login_required(login_url='login')
def appointments(request):
    logged_user = MyUser.objects.get(email=request.user)
    if logged_user.profile_description == 'Member':
        job_application_instance = Job_Application.objects.filter(job__member_user=logged_user)
    elif logged_user.profile_description == 'Caregiver':
        job_application_instance = Job_Application.objects.filter(caregiver_user=logged_user)
    context = {
        'profile_description': logged_user.profile_description,
        'appointments': job_application_instance,
    }
    if request.method == 'POST':
        if 'member_submit' in request.POST:
            appointing_caregiver = request.POST['appointing_caregiver']
            appointing_job = request.POST['appointing_job']
            work_hours = request.POST['work_hours']
            appointing_caregiver_instance = MyUser.objects.get(user_id=appointing_caregiver)
            status = request.POST['status']
            new_appointment = Appointment.objects.create(member_user=logged_user, caregiver_user=appointing_caregiver_instance, work_hours=work_hours, status=status)
            new_appointment.save()
            delete_job_application = Job_Application.objects.get(caregiver_user=appointing_caregiver_instance, job=appointing_job)
            delete_job_application.delete()
        if 'caregiver_submit' in request.POST:
            appointing_member = request.POST['appointing_member']
            appointing_job = request.POST['appointing_job']
            work_hours = request.POST['work_hours']
            appointing_member_instance = MyUser.objects.get(user_id=appointing_member)
            status = request.POST['status']
            new_appointment = Appointment.objects.create(member_user=appointing_member_instance, caregiver_user=logged_user, work_hours=work_hours, status=status)
            new_appointment.save()
            delete_job_application = Job_Application.objects.get(caregiver_user=logged_user, job=appointing_job)
            delete_job_application.delete()
    return render(request, 'main/appointments.html', context)

@login_required(login_url='login')
def settings(request):
    logged_user = MyUser.objects.get(email=request.user)
    context = {
        'logged_user': logged_user,
    }
    if request.method == 'POST':
        if 'member_settings' in request.POST:
            new_house_rules = request.POST['new_house_rules']
            member_instance = Member.objects.get(member_user=logged_user)
            member_instance.house_rules = new_house_rules
            member_instance.save()
            return redirect('profilepage')
        if 'caregiver_settings' in request.POST:
            new_hourly_rate = request.POST['new_hourly_rate']
            caregiver_instance = Caregiver.objects.get(caregiver_user=logged_user)
            caregiver_instance.hourly_rate = new_hourly_rate
            caregiver_instance.save()
            return redirect('profilepage')
    return render(request, 'main/settings.html', context)
