from django.shortcuts import render, redirect

from .forms import CheckinForm
from .models import Checkin

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
