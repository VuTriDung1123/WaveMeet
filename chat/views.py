from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Room, Participant

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('login')
    
@login_required
def home(request):
    from .models import User
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/home.html', {'users': users})

@login_required
def create_room(request):
    if request.method == 'POST':
        room = Room.objects.create(host=request.user)
        Participant.objects.create(room=room, user=request.user)
        return redirect('room_detail', room_id=room.id)
    return redirect('home')

@login_required
def join_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        if room_id:
            try:
                room = Room.objects.get(id=room_id, is_active=True)
                if room.is_locked and room.host != request.user:
                    # Prevent non-hosts from joining locked rooms
                    # For simplicity, redirect to home. In a real app, send a message.
                    return redirect('home')
                Participant.objects.get_or_create(room=room, user=request.user)
                return redirect('room_detail', room_id=room.id)
            except Room.DoesNotExist:
                # Handle room not found gracefully later
                return redirect('home')
    return redirect('home')

import time
import hmac
import hashlib
import base64
import os

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_active=True)
    # Ensure user is participant
    Participant.objects.get_or_create(room=room, user=request.user)

    # 1. Generate TURN Server Credentials (HMAC Auth)
    turn_secret = os.getenv('TURN_SECRET', 'wavemeet-secret-key-for-coturn')
    turn_url = os.getenv('TURN_URL', 'turn:turn.example.com:3478')
    
    # Expiration time for this temporary credential (e.g., 24 hours)
    ttl = 86400
    timestamp = int(time.time()) + ttl
    turn_username = f"{timestamp}:{request.user.username}"
    
    mac = hmac.new(
        turn_secret.encode('utf-8'),
        turn_username.encode('utf-8'),
        hashlib.sha1
    )
    turn_password = base64.b64encode(mac.digest()).decode('utf-8')

    context = {
        'room': room,
        'turn_url': turn_url,
        'turn_username': turn_username,
        'turn_password': turn_password,
        'is_host': request.user == room.host
    }
    
    return render(request, 'chat/room.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def toggle_room_lock(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if room.host != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    room.is_locked = not room.is_locked
    room.save()
    return JsonResponse({'success': True, 'is_locked': room.is_locked})
