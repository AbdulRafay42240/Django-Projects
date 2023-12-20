from django.shortcuts import render, HttpResponse
from main.models import addvehicle
from datetime import datetime, timedelta


# # Create your views here.
def home(request):
    if request.method == "POST":
            carname = request.POST.get('carName')
            carplate = request.POST.get('carNumberPlate')
            drivername = request.POST.get('carDriverName')
            drivernumber = request.POST.get('carDriverPhone')
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            addveh = addvehicle(
            car_name=carname,
            car_plate=carplate,
            driver_name=drivername,
            driver_contact=drivernumber,
            parking_time=formatted_datetime)
            addveh.save()
            return render(request, 'page-01.html')
    elif request.method == "GET":
        plates = addvehicle.objects.values_list('car_plate', flat=True)
        carplate = request.GET.get('carNumberPlate')
        removed_entries = addvehicle.objects.filter(car_plate=carplate).delete()
        return render(request, 'page-01.html')
    else:
        return render(request, 'page-01.html')

def add(request):
    return render(request, 'add.html')

def remove(request):
    return render(request, 'remove.html')

def bill(request):
    return render(request, 'bill.html')

def view(request):
    entries = addvehicle.objects.values('car_plate', 'car_name')
    data = {}
    for entry in entries:
        data[entry['car_plate']] = entry['car_name']
    print(data)
    return render(request, 'view.html',{'data':data})

def recipt(request):
    if request.method == "POST":
        carplate = request.POST.get('carNumberPlate')
        parking_time = addvehicle.objects.filter(car_plate=carplate).values_list('parking_time', flat=True).first()
        def calculate_parking_cost(entry_time_db, hourly_rate=5):
            current_time = datetime.now()
            entry_time = datetime.strptime(entry_time_db, "%Y-%m-%d %H:%M:%S")
            parking_duration = (current_time - entry_time).total_seconds() / 3600
            duration = current_time - entry_time
            hours, remainder = divmod(duration.seconds, 3600)
            minutes = remainder // 60
            entry_time_str = entry_time.strftime("%Y-%m-%d %I:%M %p")
            exit_time_str = current_time.strftime("%Y-%m-%d %I:%M %p")
            if parking_duration < 1:
                total_cost = 5
            else:
                rounded_hours = int(parking_duration) + (1 if parking_duration % 1 != 0 else 0)
                total_cost = rounded_hours * 5
            return [total_cost, entry_time_str, exit_time_str, hours, minutes]
        data = calculate_parking_cost(parking_time)
        cont = {'pay':data[0],
                'entry':data[1],
                'exit':data[2],
                'hrs':data[3],
                'mins':data[4],
                'car':carplate}
    return render(request, 'recipt.html', cont)
