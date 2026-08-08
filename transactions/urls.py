from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('history/', views.transaction_history_view, name='history'),
    path('export-csv/', views.export_csv_view, name='export_csv'),
]
