import csv
import datetime

from django.shortcuts import render, redirect

from .forms import CheckinForm, CSVUploadForm
from .models import Checkin, Player

from datetime import date


def home(request):
    """The home page for Challenge Weekbier."""
    return render(request, 'challenge_weekbier/home.html')


def new_checkin(request):
    print("New checkin")
    """Add a new checkin."""
    if request.method != 'POST':
        # No data submitted; create a form with date initialised to today.
        initial_data = {'date': date.today().strftime('%Y-%m-%d')}
        form = CheckinForm(initial=initial_data)
    else:
        # Post data submitted; process data.
        form = CheckinForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('challenge_weekbier:home')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'challenge_weekbier/new_checkin.html', context)


def standings(request):
    """Show the standings."""
    return render(request, 'challenge_weekbier/standings.html')


def checkins(request):
    """Show the checkins."""
    checkins = Checkin.objects.order_by('-date')
    context = {'checkins': checkins}
    return render(request, 'challenge_weekbier/checkins.html', context)


def upload_csv(request):
    def excel_date_to_datetime(serial_number):
        base_date = datetime.datetime(1900, 1, 1)
        if 1 <= serial_number <= 59:
            serial_number -= 1  # Account for the 1900 Leap Year bug
        elif 60 <= serial_number <= 61:
            serial_number -= 2  # Account for the 1900 Leap Year bug
        else:
            serial_number -= 2  # Account for the 1900 Leap Year bug and 1904 base date
            base_date = datetime.datetime(1904, 1, 1)
        return base_date + datetime.timedelta(days=serial_number)

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        print("Form: ", form)
        print("Request: ", request)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())

            next(reader)  # Skip the header row

            for row in reader:
                date_added = row[0]
                player_name = row[1]
                checkin_date = excel_date_to_datetime(int(row[2]))
                place = row[3]
                city = row[4]

                player = Player(name=player_name)
                player.save()
                checkin = Checkin(date_added=date_added, player=player, date=checkin_date, place=place, city=city)
                checkin.save()

            return render(request, 'challenge_weekbier/upload_csv.html', {'form': form})

        else:
            print(form.errors)
    else:
        form = CSVUploadForm()
    return render(request, 'challenge_weekbier/upload_csv.html', {'form': form})