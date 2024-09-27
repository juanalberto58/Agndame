from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .utils import google_calendar

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_success')
    else:
        form = AppointmentForm

    return render(request, 'book_appointment.html', {'form': form})


def book_success(request):
    return render(request, 'book_success.html') 