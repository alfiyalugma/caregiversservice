from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.registration, name='registration'),
    path('registration_member', views.registration_member, name='registration_member'),
    path('registration_caregiver', views.registration_caregiver, name='registration_caregiver'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profilepage', views.profilepage, name='profilepage'),
    path('profilepage/<str:email>/', views.profilepage, name='profilepage_otheruser'),
    path('network', views.network, name='network'),
    path('create_application', views.create_application, name='create_application'),
    path('appointments', views.appointments, name='appointments'),
    path('settings', views.settings, name='settings'),
]
