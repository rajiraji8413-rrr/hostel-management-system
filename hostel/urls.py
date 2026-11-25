
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StudentViewSet,
    RoomViewSet,
    RoomAllocationViewSet,
    FeePaymentViewSet,
    DashboardView,
    dashboard_page,
    students_page,
    rooms_page,
    allocations_page,
    payments_page,
)

# API ROUTER
router = DefaultRouter()

router.register(r'students', StudentViewSet, basename='student')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'allocations', RoomAllocationViewSet, basename='allocation')
router.register(r'payments', FeePaymentViewSet, basename='payment')


# URL PATTERNS
urlpatterns = [
    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard-page/', dashboard_page, name='dashboard_page'),

    # Student Management
    path('students-page/', students_page, name='students_page'),

    # Room Management
    path('rooms-page/', rooms_page, name='rooms_page'),

    # Room Allocation
    path('allocations-page/', allocations_page, name='allocations_page'),

    # Fee Payment
    path('payments-page/', payments_page, name='payments_page'),

    # API Endpoints
    path('', include(router.urls)),
]
