from django.shortcuts import render
import os
import requests 
import datetime 
from dotenv import load_dotenv
load_dotenv()
# Create your views here.
def home(request):
    api_key = os.getenv('OPEN_WEATHER_API_KEY')  # Grab the API key from environment variables

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Toronto'
        
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    params = {'units': 'metric'}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()

        
        # Check if 'weather' key exists in the response
        if 'weather' in data:
            describe = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            temp = data['main']['temp']
        else:
            # If 'weather' key is not present, handle the error
            describe = 'Weather data not available'
            icon = None
            temp = 0
        
    except Exception as e:
        # Handle any other exceptions (e.g., network issues)
        describe = 'Error fetching data'
        icon = None
        temp = None

    day = datetime.date.today()
    

    return render(request, 'weather/index.html', {'description': describe, 'icon': icon, 'temp': temp, 'day': day, 'city': city})
