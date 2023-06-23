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
    return render(request, 'challenge_weekbier/home.html', context)


def standings(request):
    """Show the standings."""
    players = Player.objects.all()
    context = {'players': players}
    return render(request, 'challenge_weekbier/standings.html', context)


def checkins(request):
    """Show the checkins."""
    checkins = Checkin.objects.order_by('-date')
    context = {'checkins': checkins}
    return render(request, 'challenge_weekbier/checkins.html', context)


def upload_csv(request):
    def excel_date_conversion(serial_number):
        base_date = datetime.datetime(1900, 1, 1)
        return (base_date + datetime.timedelta(days=serial_number-2)).date()

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())

            next(reader)  # Skip the header row
            # TODO: Move this to a function
            for row in reader:
                date_added = row[0]
                player_name = row[1]
                checkin_date = excel_date_conversion(int(row[2]))
                place = row[3]
                city = row[4]

                # Get player, or create if it doesn't exist
                this_player = Player.objects.filter(name=player_name)
                if this_player.exists():
                    player = this_player.first()
                else:
                    player = Player(name=player_name)
                    player.save()

                checkin = Checkin(date_added=date_added, player=player, date=checkin_date, place=place, city=city)
                checkin.save()

            return render(request, 'challenge_weekbier/upload_csv.html', {'form': form})

    else:
        form = CSVUploadForm()
    return render(request, 'challenge_weekbier/upload_csv.html', {'form': form})