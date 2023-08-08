from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,  permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import User, Banks, Accounts, History
from .serializers import UserSerializer, AccountSerializer, BanksSerializer, HistorySerializer
import random
import string

@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": True,
                "data": {
                    "username": serializer.data['username'],
                    "password": request.data.get('password')
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def custom_obtain_auth_token(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"status": False, "error": "Nombre de usuario y contraseña requeridos."}, status=400)
        
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            return Response({"status": False, "error": "Credenciales inválidas."}, status=401)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "status": True,
            "data": {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "token": token.key
            }
        })
    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def account_list(request):
    if request.method == 'POST':
        user_id = get_user_id_by_username(request.data.get('username'))
        queryset = Accounts.objects.filter(holder=user_id)
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_accounts_by_id(request):
    if request.method == 'POST':
        user_id = get_user_id_by_username(request.data.get('holder'))
        account_numbers  = Accounts.objects.filter(holder=user_id).values_list('account_number', flat=True)
        return Response({'account_numbers': list(account_numbers)}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Requiere autorización con token
def create_account(request):
    if request.method == 'POST':
        request.data['holder'] = get_user_id_by_username(request.data.get('holder'))
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            history_data = {
                'transactionType': 'Cuenta creada',
                'value': request.data['balance'], 
                'account': account.id,
                'user': request.data['holder'],
                'track_id': generate_transaction_track_id()
            }
            history_serializer = HistorySerializer(data=history_data)
            if history_serializer.is_valid():
                history_serializer.save()

            return Response({'status': True, 'message': 'Cuenta creada exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_user_id_by_username(username):
    try:
        user = User.objects.get(username=username)
        return user.id
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=404)
    
def generate_transaction_track_id():
    prefix = "LCL"
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    track_id = prefix + random_chars
    return track_id


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def banks_list(request):
    if request.method == 'GET':
        queryset = Banks.objects.all()
        serializer = BanksSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_balance(request):
    if request.method == 'POST':
        account_number = request.data['account_number']
        amount = float(request.data['balance'])
        request.data['holder'] = get_user_id_by_username(request.data.get('holder'))
        try:
            account = get_object_or_404(Accounts, account_number=account_number)
            account.balance = float(account.balance) + amount
            account.save()
            transaction_code = generate_transaction_track_id()
            history_data = {
                'transactionType': 'Consignación',
                'value': request.data['balance'], 
                'account': account.id,
                'user': request.data['holder'],
                'track_id': transaction_code
            }
            print(history_data)
            history_serializer = HistorySerializer(data=history_data)
            if history_serializer.is_valid():
                history_serializer.save()
            else:
                errors = history_serializer.errors
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'status':True,'account':account_number ,'code': transaction_code, 'new_balance': account.balance }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subtract_balance(request):
    if request.method == 'POST':
        account_number = request.data['account_number']
        amount = float(request.data['balance'])
        request.data['holder'] = get_user_id_by_username(request.data.get('holder'))
        try:
            account = get_object_or_404(Accounts, account_number=account_number)
            if account.balance >= amount:
                account.balance = float(account.balance) - amount
                account.save()
                transaction_code = generate_transaction_track_id()
                history_data = {
                    'transactionType': 'Retirar',
                    'value': request.data['balance'], 
                    'account': account.id,
                    'user': request.data['holder'],
                    'track_id': transaction_code
                }
                history_serializer = HistorySerializer(data=history_data)
                if history_serializer.is_valid():
                    history_serializer.save()
                else:
                    errors = history_serializer.errors
                    return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'status':True,'account':account_number ,'code': transaction_code,      'new_balance': account.balance }, status=status.HTTP_200_OK)
            else:
                return Response({'status':True,'balance': account.balance}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_balance_by_account(request):
    if request.method == 'POST':
        account_number = request.data.get('account_number')
        balance  = Accounts.objects.filter(account_number=account_number).values_list('balance', flat=True)
        return Response({'balance': balance[0]}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_activity_by_user(request):
    if request.method == 'POST':    
        user_id = get_user_id_by_username(request.data.get('holder'))
        user_history = History.objects.filter(user_id=user_id).select_related('account').order_by('-date_time')
        serialized_history = [] 
        for history_entry in user_history:
            serialized_entry = {
                'transactionType': history_entry.transactionType,
                'date_time': history_entry.date_time,
                'value': history_entry.value,
                'account_number': history_entry.account.account_number,
                'track_id': history_entry.track_id
            }
            serialized_history.append(serialized_entry)
        return Response(serialized_history, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)