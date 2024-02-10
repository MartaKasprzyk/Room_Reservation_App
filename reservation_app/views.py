from django.shortcuts import render, redirect
from reservation_app.models import Room, Reservation
from django.views import View
import datetime


def home(request):
    return render(request, 'base.html')


class AddRoom(View):

    def context_data(self):
        rooms = Room.objects.all()
        context = {'rooms': rooms}
        return context

    def get(self, request):
        context = self.context_data()
        return render(request, 'add_room.html', context)

    def post(self, request):
        name = str(request.POST.get('name'))
        seats = int(request.POST.get('seats'))
        projector = request.POST.get('projector')

        if name is not '':
            if Room.objects.filter(name=name).exists():
                message = f'Room already exists. Try again.'
                return render(request, 'add_room.html', {'message': message})
            else:
                if seats < 0:
                    message = f'Seats number must be greater than zero.'
                    return render(request, 'add_room.html', {'message': message})
                else:
                    if projector == 'True':
                        projector = True
                    else:
                        projector = False
                    Room.objects.create(name=name, seats=seats, projector=projector)
                    message = f'Room {name} added successfully.'
                    return render(request, 'add_room.html', {'message': message})
        else:
            message = f'Input room name.'
            return render(request, 'add_room.html', {'message': message})


class ViewAvailableRooms(View):

    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'available_rooms.html', {"rooms": rooms})


class DeleteRoom(View):

    def get(self, request, id):
        room = Room.objects.get(id=id)
        room.delete()
        message = f'Room {room.name} deleted successfully.'
        rooms = Room.objects.all()
        return render(request, 'available_rooms.html', {'message': message, "rooms": rooms})


class ModifyRoom(View):

    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(request, "modify_room.html", {'room': room})

    def post(self, request, id):
        room = Room.objects.get(id=id)
        name = str(request.POST.get('name'))
        seats = int(request.POST.get('seats'))
        projector = request.POST.get('projector')

        if name is not '':
            if seats < 0:
                message = f'Seats number must be greater than zero.'
                return render(request, 'modify_room.html', {'message': message})
            else:
                if projector == 'True':
                    projector = True
                else:
                    projector = False
                room.name = name
                room.seats = seats
                room.projector = projector
                if Room.objects.filter(name=name, seats=seats, projector=projector).exists():
                    message = f'This room already exists.'
                    return render(request, 'modify_room.html', {'message': message})
                else:
                    room.save()
                    message = f'Room {room.name} modified successfully.'
                    rooms = Room.objects.all()
                    return render(request, 'modify_room.html', {'message': message, "rooms": rooms})
        else:
            message = f'Input room name.'
            return render(request, 'modify_room.html', {'message': message})


class ReserveRoom(View):

    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(request, "reserve_room.html", {'room': room})

    def post(self, request, id):
        room = Room.objects.get(id=id)
        rooms = Room.objects.all()
        date = datetime.date.fromisoformat(request.POST.get('date'))
        comment = request.POST.get('comment')

        if Reservation.objects.filter(room_id=room, date=date).exists():
            message = f'Room already reserved.'
            return render(request, 'reserve_room.html', {'message': message})
        else:
            if date < datetime.date.today():
                message = f'Incorrect date. Can not reserve a room for date in the past!'
                return render(request, 'reserve_room.html', {'message': message})
            else:
                Reservation.objects.create(date=date, room_id=room, comment=comment)
                return render(request, 'available_rooms.html', {"rooms": rooms})


class RoomView(View):

    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(request, 'view_room.html', {'room': room})


class RoomSearch(View):

    def get(self, request):
        name = request.GET.get('name', '')
        seats = request.GET.get('seats', '')
        seats = int(seats) if seats else 0
        projector = request.GET.get('projector', '')
        string_date = str(request.GET.get('date')) if request.GET.get('date') else ''
        try:
            iso_format_string = datetime.date.fromisoformat(string_date)
            date = iso_format_string
        except ValueError:
            date = ''

        rooms = Room.objects.all()

        if projector:
            rooms = rooms.filter(projector=projector)
        if seats:
            rooms = rooms.filter(seats__gte=seats)
        if name:
            rooms = rooms.filter(name__icontains=name)
        if date:
            for room in rooms:
                if room.get_reservations().filter(date=date):
                    rooms = rooms.exclude(id=room.id)


        return render(request, 'search_room.html', {'rooms': rooms})
