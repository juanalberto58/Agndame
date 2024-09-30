from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .utils.google_calendar import GoogleCalendarManager
from datetime import datetime, timedelta

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()

            calendar_manager = GoogleCalendarManager()

            event_data = {
                    'summary': f'Cita con {appointment.name_client} {appointment.lastname_client}',
                    'start_time': datetime.combine(appointment.date, appointment.hour).strftime('%Y-%m-%dT%H:%M:%S+02:00'),
                    'end_time': (datetime.combine(appointment.date, appointment.hour) + timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%S+02:00'),
                    'timezone': 'Europe/Madrid',  
                    'attendees': ['cliente@example.com'],  
            }
            

            calendar_manager.create_event(
                event_data['summary'],
                event_data['start_time'],
                event_data['end_time'],
                event_data['timezone'],
                event_data['attendees']
            )
            
            return redirect('book_success')
    else:
        form = AppointmentForm

    return render(request, 'book_appointment.html', {'form': form})


def book_success(request):
    return render(request, 'book_success.html') 