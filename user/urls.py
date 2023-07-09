from django.contrib.auth.views import LoginView
from django.urls import path
from . import views as v


app_name = 'user'

urlpatterns = [
    path('sign_up/', v.register, name='register'),
    path('login/', v.sign_in, name='login'),
    path('patient/dashboard', v.pat_dashboard, name='dashboard'),
    path('patient/make_request', v.make_request, name='make_request'),
    path('patient/my-request', v.my_request_view, name='my_request'),
    path('log_out', v.log_out, name='log_out'),
    path('donor/donate', v.donate_blood, name='donate'),
    path('donor/dashboard', v.donor_dashboard, name='d_dashboard'),
    path('donor/patients', v.donor_patients, name='d_patients'),

    path('admin-dashboard', v.admin_dashboard_view, name='admin-dashboard'),
    path('blood-update', v.update_blood_amount, name='blood-update'),
    path('admin-donor', v.admin_donor_view, name='admin-donor'),
    path('admin-request', v.admin_request_view, name='admin-request'),
    path('admin-donation', v.admin_donation_view, name='admin-donation'),
    path('update-approve-status/<int:pk>', v.update_approve_status_view, name='update-approve-status'),
    path('update-reject-status/<int:pk>', v.update_reject_status_view, name='update-reject-status'),
    path('approve-donation/<int:pk>', v.approve_donation_view, name='approve-donation'),
    path('reject-donation/<int:pk>', v.reject_donation_view, name='reject-donation'),
    path('admin-request-history', v.admin_request_history_view, name='admin-request-history'),
    path('admin-patient', v.admin_patient_view, name='admin-patient'),
    path('update-user/<int:pk>', v.update_user_view, name='update-user'),
    path('delete_donor/<int:pk>', v.delete_donor, name='delete_donor'),



]


