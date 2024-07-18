from datetime import timedelta
from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LogoutView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import UAVListing
from rest_framework.decorators import api_view
from .serializers import UAVListingSerializer
from .models import UAV, RentalRecord
CustomUser = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            return Response({
                "user": UserSerializer(user).data,
                "message": "User registered successfully."
            }, status=status.HTTP_201_CREATED)
        return Response({
            "errors": form.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/register.html')


from rest_framework.authtoken.models import Token

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)  
            login(request, user)
            redirect_url = '/accounts/seller-dashboard/' if user.user_type == 'seller' else '/accounts/user-dashboard/'
            return Response({
                "message": "Login successful!",
                "token": token.key,
                "redirect_url": redirect_url
            }, status=200)
        else:
            return Response(serializer.errors, status=400)

    def get(self, request, format=None):
        return render(request, 'accounts/login.html')

def home(request):
    return render(request, 'accounts/home.html')


def seller_dashboard(request):
    return render(request, 'accounts/seller_dashboard.html')

def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')




from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UAV
from .serializers import UAVSerializer


class UAVViewSet(viewsets.ModelViewSet):
    queryset = UAV.objects.all()
    serializer_class = UAVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UAV.objects.filter(owner=self.request.user)
        return UAV.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def toggle_availability(self, request, pk=None):
        uav = self.get_object()
        uav.is_available = not uav.is_available
        uav.save()
        return Response({'status': 'availability toggled'})    
    
    @action(detail=True, methods=['post'])
    def list_uav(self, request, pk=None):
        uav = self.get_object()
        price = request.data.get('price')

        if price is None:
            return Response({'error': 'Price is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            return Response({'error': 'Valid price is required'}, status=status.HTTP_400_BAD_REQUEST)

        UAVListing.objects.update_or_create(uav=uav, defaults={'price': price})
        return Response({'status': 'UAV listed'})

    @action(detail=True, methods=['post'])
    def unlist_uav(self, request, pk=None):
        uav = self.get_object()
        UAVListing.objects.filter(uav=uav).delete()
        return Response({'status': 'UAV unlisted'})
    @api_view(['GET'])
    def listed_uavs(request):
        listed_uavs = UAV.objects.filter(listing__is_listed=True)
        serializer = UAVSerializer(listed_uavs, many=True)
        return Response(serializer.data)
    
from django.db.models import Q
from rest_framework import generics
from .models import UAV, RentalRecord
from .serializers import UAVSerializer
from django.db.models import Subquery, OuterRef

class ListedUAVsView(generics.ListAPIView):
    serializer_class = UAVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and end_date:
            conflicting_uavs = RentalRecord.objects.filter(
                status__in=['pending', 'active'],
                start_date__lt=end_date,
                end_date__gt=start_date
            ).values('uav_id')

            return UAV.objects.exclude(id__in=Subquery(conflicting_uavs)).annotate(
                current_rental_status=Subquery(
                    RentalRecord.objects.filter(
                        uav=OuterRef('pk'),
                        status__in=['pending', 'rented']
                    ).values('status')[:1]
                ),
                current_rental_id=Subquery(
                    RentalRecord.objects.filter(
                        uav=OuterRef('pk'),
                        status__in=['pending', 'rented']
                    ).values('id')[:1]
                ),
                current_renter_id=Subquery(
                    RentalRecord.objects.filter(
                        uav=OuterRef('pk'),
                        status='pending'
                    ).values('user_id')[:1]
                )
            )
        else:
            return UAV.objects.annotate(
                current_rental_status=Subquery(
                    RentalRecord.objects.filter(
                        uav=OuterRef('pk'),
                        status__in=['pending', 'rented']
                    ).values('status')[:1]
                ),
                current_rental_id=Subquery(
                    RentalRecord.objects.filter(
                        uav=OuterRef('pk'),
                        status__in=['pending', 'rented']
                    ).values('id')[:1]
                ),
                current_renter_id=Subquery(
                    RentalRecord.objects.filter(
                        uav=OuterRef('pk'),
                        status='pending'
                    ).values('user_id')[:1]
                )
            )



    from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import UAV, RentalRecord, CustomUser
from .serializers import RentalRecordSerializer, UAVSerializer
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rent_uav(request):
    user = request.user
    uav_id = request.data.get('uav_id')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    days = request.data.get('days')
    total_price = request.data.get('total_price')

    try:
        uav = UAV.objects.get(id=uav_id)
        new_rental = RentalRecord(
            uav=uav,
            user=user,
            start_date=start_date,
            end_date=end_date,
            status='pending'
        )

        if new_rental.check_date_conflict(start_date, end_date):
            return Response({"error": "The selected date range conflicts with an existing rental."},
                            status=status.HTTP_400_BAD_REQUEST)

        new_rental.save()
        return Response({"rental_id": new_rental.id}, status=status.HTTP_201_CREATED)

    except UAV.DoesNotExist:
        return Response({"error": "UAV not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_rental_status(request, rental_id):
    try:
        rental = RentalRecord.objects.get(id=rental_id, user=request.user)
        return Response({'status': rental.status}, status=status.HTTP_200_OK)
    except RentalRecord.DoesNotExist:
        return Response({'error': 'Rental record not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_rental_status(request, rental_id):
    try:
        rental = RentalRecord.objects.get(id=rental_id)
        rental.status = request.data.get('status', 'rented')
        rental.save()
        return Response({'message': 'Rental status updated'}, status=status.HTTP_200_OK)
    except RentalRecord.DoesNotExist:
        return Response({'error': 'Rental record not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_rental(request, rental_id):
    try:
        rental = RentalRecord.objects.get(id=rental_id, user=request.user, status='pending')
        rental.delete()
        return Response({'message': 'Rental cancelled successfully'}, status=status.HTTP_204_NO_CONTENT)
    except RentalRecord.DoesNotExist:
        return Response({'error': 'Rental record not found or not cancellable'}, status=status.HTTP_404_NOT_FOUND)

class RentalRecordListView(generics.ListAPIView):
    serializer_class = RentalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RentalRecord.objects.filter(uav__owner=self.request.user, status='pending')


@api_view(['POST'])
def update_rental_status(request, pk):
    try:
        rental = RentalRecord.objects.get(pk=pk, uav__owner=request.user)
        new_status = request.data.get('status')  
        if new_status in ['active', 'rejected']:
            rental.status = new_status
            rental.save()
            return Response({'message': 'Rental status updated.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    except RentalRecord.DoesNotExist:
        return Response({'error': 'Rental record not found'}, status=status.HTTP_404_NOT_FOUND)
    



class AllRentalRecordsView(generics.ListAPIView):
    serializer_class = RentalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RentalRecord.objects.filter(uav__owner=self.request.user).order_by('-start_date')    
    
class UserRentalRecordsView(generics.ListAPIView):
    serializer_class = RentalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RentalRecord.objects.filter(user=self.request.user).order_by('-start_date')


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm
from django.contrib import messages




@login_required
def membership(request):
    form = CustomUserChangeForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile successfully updated.')
                return redirect('membership')
            else:
                messages.error(request, f'Error updating profile: {form.errors}')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password successfully changed.')
                return redirect('membership')
            else:
                messages.error(request, f'Error changing password: {password_form.errors}')  

    context = {
        'form': form,
        'password_form': password_form
    }
    return render(request, 'accounts/membership.html', context)

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('login')


@login_required
def membershipseller(request):
    form = CustomUserChangeForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile successfully updated.')
                return redirect('membershipseller')
            else:
                messages.error(request, f'Error updating profile: {form.errors}') 
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password successfully changed.')
                return redirect('membershipseller')
            else:
                messages.error(request, f'Error changing password: {password_form.errors}') 

    context = {
        'form': form,
        'password_form': password_form
    }
    return render(request, 'accounts/membershipseller.html', context)


def landing_page(request):
    return render(request, 'accounts/landing_page.html')