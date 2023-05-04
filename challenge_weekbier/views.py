from django.shortcuts import render, redirect

from .forms import CheckinForm


def home(request):
    """The home page for Challenge Weekbier."""
    return render(request, 'challenge_weekbier/home.html')


def new_checkin(request):
    """Add a new checkin."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CheckinForm()
    else:
        # Post data submitted; process data.
        form = CheckinForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('challenge_weekbier:home')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'challenge_weekbier/new_checkin.html', context)

