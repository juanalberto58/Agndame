from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class Worker(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

class Appointment(models.Model):
    name_client = models.CharField(max_length=100)
    lastname_client = models.CharField(max_length=100)
    date = models.DateField()
    hour = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cita para {self.name_client} {self.lastname_client} - {self.date} {self.hour}"



