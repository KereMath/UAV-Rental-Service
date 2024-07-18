# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UAVViewSet, RegisterView, LoginView, LogoutView, home, seller_dashboard, user_dashboard, ListedUAVsView
from .views import rent_uav  
from .views import membershipseller, landing_page
from .views import check_rental_status, update_rental_status, cancel_rental, RentalRecordListView, AllRentalRecordsView, UserRentalRecordsView, membership, delete_account  
router = DefaultRouter()
router.register(r'uavs', UAVViewSet, basename='uav')

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('home/', home, name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('seller-dashboard/', seller_dashboard, name='seller_dashboard'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),
    path('api/uavs/listed/', ListedUAVsView.as_view(), name='listed-uavs'),
    path('api/rent_uav/', rent_uav, name='rent-uav'),  
    path('api/rentals/<int:rental_id>/status/', check_rental_status, name='check-rental-status'),
    path('api/rentals/<int:rental_id>/update_status/', update_rental_status, name='update-rental-status'),
    path('api/', include(router.urls)),
    path('api/rentals/<int:rental_id>/cancel/', cancel_rental, name='cancel-rental'),
       path('api/rental_records/', RentalRecordListView.as_view(), name='rental-records'),
    path('api/rental_records/<int:pk>/update_status/', update_rental_status, name='update-rental-status'),
    path('api/all_rental_records/', AllRentalRecordsView.as_view(), name='all-rental-records'),
    path('membership/', membership, name='membership'),
    path('membershipseller/', membershipseller, name='membershipseller'),

    path('delete-account/', delete_account, name='delete_account'),
    path('api/user_rental_records/', UserRentalRecordsView.as_view(), name='user-rental-records'),


]
