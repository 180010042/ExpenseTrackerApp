from django.urls import path
from ExpenseTrackerApp import views

urlpatterns = [
    path('register', views.register, name = 'register'),
    path('login', views.login_user, name = 'login'),
    path('login_again', views.login_again, name = 'login_again'),
    path('logout', views.logout_user, name = 'logout'),
    path('transaction', views.add_transaction, name = 'transaction'),
    path('transaction-history', views.transaction_history, name = 'transaction_history'),
    path('delete/<int:id>/', views.delete_data, name = 'delete_data'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('change-password', views.change_password, name = 'change_password'),
    path('report', views.report, name = 'report'),
    path('current-month-amount', views.current_month_amount, name = 'current_month_amount'),
    path('previous-month-amount', views.previous_month_amount, name = 'current_month_amount'),
    path('current-month-link', views.current_month_link, name = 'current_month_link'),
    path('previous-month-link', views.previous_month_link, name = 'current_month_link'),
    path('current-month-report', views.current_month_report, name = 'current_month_report'),
    path('previous-month-report', views.previous_month_report, name = 'current_month_report'),
    path('daywise-current-month-report', views.daywise_current_month_report, name = 'daywise_current_month_report'),
    path('daywise-previous-month-report', views.daywise_previous_month_report, name = 'daywise_current_month_report'),
    path('current-month-report-display', views.current_month_report_display, name = 'current_month_report_display'),
    path('previous-month-report-display', views.previous_month_report_display, name = 'previous_month_report_display'),
    path('daywise-current-month-report-display', views.daywise_current_month_report_display, name = 'daywise_current_month_report_display'),
    path('daywise-previous-month-report-display', views.daywise_previous_month_report_display, name = 'daywise_previous_month_report_display'),
]
