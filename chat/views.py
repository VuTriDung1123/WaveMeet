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
    return render(request, 'chat/home.html')

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
                Participant.objects.get_or_create(room=room, user=request.user)
                return redirect('room_detail', room_id=room.id)
            except Room.DoesNotExist:
                # Handle room not found gracefully later
                return redirect('home')
    return redirect('home')

from livekit import api
import os

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_active=True)
    Participant.objects.get_or_create(room=room, user=request.user)

    # Generate LiveKit Token
    # Make sure to set these env vars in production!
    livekit_api_key = os.getenv('LIVEKIT_API_KEY', 'devkey')
    livekit_api_secret = os.getenv('LIVEKIT_API_SECRET', 'secret')
    
    token = api.AccessToken(livekit_api_key, livekit_api_secret)
    token.with_identity(request.user.username)
    token.with_name(request.user.username)
    token.with_grants(api.VideoGrants(
        room_join=True,
        room=str(room.id)
    ))
    
    jwt_token = token.to_jwt()

    return render(request, 'chat/room.html', {
        'room': room,
        'livekit_token': jwt_token,
        'livekit_url': os.getenv('LIVEKIT_URL', 'ws://127.0.0.1:7880')
    })
