from django.db import models

class WeatherForecast(models.Model):
    city = models.CharField(max_length=255)
    date = models.DateField()
    condition = models.CharField(max_length=255)
    temperature = models.FloatField()
    maxtemp = models.FloatField(null=True, blank=True)  
    mintemp = models.FloatField(null=True, blank=True)
    totalprec = models.FloatField(null=True, blank=True)
    sunrise = models.TimeField(null=True, blank=True)
    sunset = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('city', 'date')  #Prevent duplicate entries for the same city and date

    def __str__(self):
        return f"{self.city} - {self.date}"