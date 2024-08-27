from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import User
import json

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists'})

        user = User(username=username, password=make_password(password), email=email)
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User registered successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return JsonResponse({'status': 'success', 'message': 'Login successful'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def update_points(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        points = data.get('points')

        try:
            user = User.objects.get(username=username)
            user.points += points
            user.save()
            return JsonResponse({'status': 'success', 'message': 'Points updated successfully', 'total_points': user.points})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def get_leaderboard(request):
    if request.method == 'GET':
        users = User.objects.all().order_by('-points')[:8]  # Get top 8 users
        leaderboard_data = [
            {'username': user.username, 'points': user.points}
            for user in users
        ]
        return JsonResponse(leaderboard_data, safe=False)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})