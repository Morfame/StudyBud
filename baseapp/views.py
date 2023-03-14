from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Super Yacht Chat'},
#     {'id': 3, 'name': 'Ruby on Rails'},
# ]

def home(request):
    qry = request.GET.get('qry') if request.GET.get('qry') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=qry) |  # i contains means not case sensitive many other options to research
        Q(name__icontains=qry) | #& additionally | means or
        Q(description__icontains=qry)
        )
    topics = Topic.objects.all() #filter how many you want to see in side bar by most content of other such things
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'baseapp/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'baseapp/room.html', context)

def createRoom(request):
    form = RoomForm()
    
    if request.method == 'POST':
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'baseapp/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method =='POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'baseapp/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'baseapp/delete.html', {'obj':room})
