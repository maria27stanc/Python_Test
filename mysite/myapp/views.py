import requests
from django.shortcuts import render
from datetime import date, timedelta
from .models import WeatherForecast
from datetime import datetime
import json

def get_weather(request):
    weather_data = None
    error_message = None

    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            api_key = '82d4f53b5f6a4d57941195027251102'
            api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

            today = date.today()

            forecast_data = []


            for i in range(-5, 4):  #5 past days, 3 future
                target_date = today + timedelta(days=i)
                date_str = target_date.strftime("%Y-%m-%d") #Format date for API

                api_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&dt={date_str}"


                try:
                    response = requests.get(api_url)
                    response.raise_for_status()
                    data = response.json()
                    if data['forecast']['forecastday']:
                        forecast_data.append(data)

                except requests.exceptions.RequestException as e:
                    error_message = f"Error fetching weather data: {e}"
                    print(f"API request error: {e}")
                    break


            if not error_message:
                weather_data = forecast_data

        if not error_message and weather_data:  #Save to database if no errors and data exists
            for day_data in weather_data:
                forecast_date = date.fromisoformat(day_data['forecast']['forecastday'][0]['date']) #Convert string date to date object

                
                try:
                    #Get or create: Try to get existing data, create if doesn't exist
                    forecast_day = day_data.get('forecast', {}).get('forecastday', [{}])[0] # Get the forecast day data safely
                    
                    day = forecast_day.get('day', {}) #Get the day data safely
                    astro = forecast_day.get('astro', {})
                    
                    sunrise_time = datetime.strptime(astro.get('sunrise'), '%I:%M %p').time()
                    sunset_time = datetime.strptime(astro.get('sunset'), '%I:%M %p').time()
                    
                    condition = day.get('condition', {}).get('text')  # Get the text safely
                    temperature = day.get('avgtemp_c')
                    maxtemp = day.get('maxtemp_c')
                    mintemp = day.get('mintemp_c')
                    totalprec = day.get('totalprecip_mm')
                    sunrise = sunrise_time
                    sunset = sunset_time
    
                    if condition and temperature:  #Only save if condition & temp are available
                        forecast_entry, created = WeatherForecast.objects.get_or_create(
                            city=day_data['location']['name'],
                            date=forecast_date,
                            defaults={
                            'condition': condition,
                            'temperature': temperature,
                            'maxtemp': maxtemp,
                            'mintemp': mintemp,
                            'totalprec': totalprec,
                            'sunrise': sunrise,
                            'sunset': sunset,
                            }
                        )

                        if not created:  #If exists, update it
                            forecast_entry.condition = condition
                            forecast_entry.temperature = temperature
                            forecast_entry.maxtemp = maxtemp
                            forecast_entry.mintemp = mintemp
                            forecast_entry.totalprec = totalprec
                            forecast_entry.sunrise = sunrise
                            forecast_entry.sunset = sunset
                            forecast_entry.save()

                    else:
                        print(f"Incomplete data for {forecast_date}: condition or temperature missing")

                except Exception as e:
                    print(f"Error saving to database: {e}")


    return render(request, 'myapp/weather.html', {'weather_data': weather_data, 'error_message': error_message})


def location_data(request):
    locations = WeatherForecast.objects.values_list('city', flat=True).distinct()  #Get locations

    selected_location = request.GET.get('location')  #Get selected location from dropdown

    weather_data = None
    if selected_location:
        weather_data = WeatherForecast.objects.filter(city=selected_location).order_by('date') # Order by date


    if weather_data:
        #Prepare data for Chart.js
        chart_data = {  # Double quotes here are crucial!
            "labels": [str(data.date) for data in weather_data],
            "datasets": [{
                "label": "Temperature",  # Double quotes here
                "data": [data.temperature for data in weather_data],
                "borderColor": "orange",
                "borderWidth": 1,
                "fill": False,
                "tension": 0.4
            }]
        }
                
        
        
        chart_data_json = json.dumps(chart_data)
        
        #debug
        print(chart_data_json) 
        
        return render(request, 'myapp/location_data.html', {
        'locations': locations,
        'selected_location': selected_location,
        'weather_data': weather_data,
        'chart_data': chart_data_json
    })
    else:
        chart_data = None
        return render(request, 'myapp/location_data.html', {
        'locations': locations,
        'selected_location': selected_location,
        'weather_data': weather_data,
        'chart_data': chart_data
    })