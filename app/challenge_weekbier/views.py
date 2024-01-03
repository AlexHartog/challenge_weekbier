import csv
import datetime
from datetime import date, timedelta

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import CheckinForm, CSVUploadForm
from .models import Checkin, Player


def home(request):
    """The home page for Challenge Weekbier."""
    return render(request, "challenge_weekbier/new_checkin.html")


def new_checkin(request):
    """Add a new checkin."""
    if request.method != "POST":
        # No data submitted; create a form with date initialised to today.
        initial_data = {"date": date.today().strftime("%Y-%m-%d")}
        form = CheckinForm(initial=initial_data)
    else:
        # Post data submitted; process data.
        form = CheckinForm(data=request.POST)
        if form.is_valid():
            form.save()
            return render(
                request, "challenge_weekbier/succesful_checkin.html", {"form": form}
            )

    # Display a blank or invalid form.
    context = {"form": form}
    return render(request, "challenge_weekbier/new_checkin.html", context)


def standings(request):
    """Show the standings."""
    players = sorted(
        Player.objects.all(),
        key=lambda player: (player.num_weeks_scored(), player.score()),
        reverse=True,
    )
    context = {"players": players}
    return render(request, "challenge_weekbier/standings.html", context)


def checkins(request):
    context = {"checkins": Checkin.objects.ordered_by_date()}
    return render(request, "challenge_weekbier/checkins.html", context)


def statistics(request):
    players = Player.objects.all()

    current_week_number = (date.today() + timedelta(days=1)).isocalendar()[1]
    weeks = dict(
        sorted(
            {num: {} for num in range(1, current_week_number + 1)}.items(), reverse=True
        )
    )

    for player in players:
        for week_number in weeks.keys():
            weeks[week_number][player.name] = 0
        for checkin in player.get_valid_checkins():
            week_number = (checkin.date + timedelta(days=1)).isocalendar()[1]
            if week_number not in weeks.keys():
                weeks[week_number] = {}
            weeks[week_number][player.name] = weeks[week_number].get(player.name, 0) + 1

    context = {
        "weeks": weeks,
        "players": players,
        "current_week_number": current_week_number,
    }
    return render(request, "challenge_weekbier/statistics.html", context)


def upload_csv(request):
    def excel_date_conversion(serial_string):
        serial_number = int(serial_string.replace(",", "").replace(".", "")[:5])
        base_date = datetime.datetime(1900, 1, 1)
        return (base_date + datetime.timedelta(days=serial_number - 2)).date()

    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file.read().decode("utf-8").splitlines())

            next(reader)  # Skip the header row
            # TODO: Move this to a function
            for row in reader:
                date_added = row[0]
                player_name = row[1]
                checkin_date = excel_date_conversion(row[2])
                place = row[3]
                city = row[4]

                # Get player, or create if it doesn't exist
                this_player = Player.objects.filter(name=player_name)
                if this_player.exists():
                    player = this_player.first()
                else:
                    player = Player(name=player_name)
                    player.save()

                checkin_exists = Checkin.objects.filter(
                    player=player, date=checkin_date, place=place, city=city
                ).exists()

                if not checkin_exists:
                    checkin = Checkin(
                        date_added=date_added,
                        player=player,
                        date=checkin_date,
                        place=place,
                        city=city,
                    )
                    checkin.save()

            return render(request, "challenge_weekbier/upload_csv.html", {"form": form})

    else:
        form = CSVUploadForm()
    return render(request, "challenge_weekbier/upload_csv.html", {"form": form})


@require_http_methods(["POST"])
def filter_checkins(request):
    player = request.POST["filter_player"]
    place = request.POST["filter_place"]
    city = request.POST["filter_city"]

    context = {
        "checkins": Checkin.objects.filtered(player=player, place=place, city=city)
    }

    return render(request, "filter_checkins.html", context)


def check_city(request):
    """Check if this player already checked in in these city."""
    player_id = request.POST.get("player", None)
    city = request.POST.get("city", None)

    if player_id and city:
        checkin = Checkin.objects.filter_exact(player_id=player_id, city=city).first()
    else:
        checkin = None

    context = {"checkin": checkin}
    return render(request, "checkin_messages.html", context)
