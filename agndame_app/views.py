from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .utils.google_calendar import GoogleCalendarManager
from datetime import datetime, timedelta
from .utils.google_sheet import GoogleSheetManager
from .utils.email import EmailManager

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()

            # Creamos un evento en google calendar
            calendar_manager = GoogleCalendarManager()
            calendar_manager.create_event(
                f'Cita con {appointment.name_client} {appointment.lastname_client}',
                datetime.combine(appointment.date, appointment.hour).strftime('%Y-%m-%dT%H:%M:%S+02:00'),
                (datetime.combine(appointment.date, appointment.hour) + timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%S+02:00'),
                'Europe/Madrid',
                [appointment.email]
            )

            # Creamos la cita en nuestra hoja de calculo
            sheet_manager = GoogleSheetManager()
            sheet_manager.insert_data_sheet('Sheet1', [appointment.name_client, appointment.lastname_client, appointment.email, appointment.date.strftime('%d-%m-%Y'), appointment.hour.strftime('%H:%M:%S'), appointment.category.name, appointment.service.name, appointment.worker.name, appointment.note])

            # Mandamos un correo de confirmacion de la cita
            email_manager = EmailManager()
            email_manager.send_mail(appointment)

            return redirect('book_success')
    else:
        form = AppointmentForm

    return render(request, 'book_appointment.html', {'form': form})


def book_success(request):
    return render(request, 'book_success.html') 