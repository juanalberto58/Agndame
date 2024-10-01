import smtplib 
from email.message import EmailMessage 
from decouple import config

class EmailManager:
    def send_mail(self, appointment):
        email_subject = f"Confirmación de Cita {appointment.name_client} {appointment.lastname_client}"
        sender_email_address = "pruebaapidjango@gmail.com"
        receiver_email_address = {appointment.email}
        email_smtp = "smtp.gmail.com"
        email_password = config('EMAIL_PASSWORD')

        message = EmailMessage()

        message['Subject'] = email_subject
        message['From'] = sender_email_address
        message['To'] = receiver_email_address

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                .container {{
                    width: 100%;
                    padding: 20px;
                    background-color: #ffffff;
                    margin: 0 auto;
                    max-width: 600px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #333333;
                }}
                p {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #666666;
                }}
                .footer {{
                    margin-top: 30px;
                    font-size: 12px;
                    color: #999999;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Estimado {appointment.name_client} {appointment.lastname_client},</h1>

                <p>
                    Esperamos que se encuentre bien. Queremos confirmar la cita que ha solicitado en nuestra peluquería. 
                    Agradecemos la confianza que ha depositado en nosotros y estamos ansiosos de atenderle. Detalles de la cita:
                </p>

                <ul>
                    <li><strong>Fecha:</strong> {appointment.date}</li>
                    <li><strong>Hora:</strong> {appointment.hour}</li>
                    <li><strong>Servicio:</strong> {appointment.service.name}</li>
                    <li><strong>Ubicación:</strong> 800 Howard St., San Francisco, CA 94103</li>
                </ul>

                <p>
                    Por favor, recuerde llegar unos minutos antes de su cita para que podamos ofrecerle el mejor servicio posible. 
                    Si necesita cancelar o reprogramar su cita por alguna razón, le agradecemos que nos contacte con anticipación. 
                    Si tiene alguna pregunta o inquietud antes de la cita, no dude en ponerse en contacto con nosotros a través de 
                    pruebaapidjango@gmail.com. Estamos aquí para ayudarle.
                </p>

                <p>¡Esperamos poder brindarle una experiencia excepcional en nuestra peluquería!</p>
                <p><strong>El equipo de Peluquería Bella Vida</strong></p>

                <div class="footer">
                    <p>
                        Peluquería Bella Vida, 800 Howard St., San Francisco, CA 94103<br>
                        Teléfono: (123) 456-7890 | Correo: info@yourcompany.com
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        message.set_content("Este correo contiene contenido HTML.", subtype='plain')
        message.add_alternative(html_content, subtype='html')

        server = smtplib.SMTP(email_smtp, '587')
        server.ehlo()  
        server.starttls()  
        server.login(sender_email_address, email_password)
        server.send_message(message)
        server.quit()  
