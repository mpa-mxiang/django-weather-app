from django.shortcuts import render
import os
import requests 
import datetime 
from dotenv import load_dotenv
load_dotenv()
# Create your views here.
def home(request):
    # Grab the API key from environment variables
    weather_api_key = os.getenv('OPEN_WEATHER_API_KEY')  
    search_api_key = os.getenv('SEARCH_ENGINE_API_KEY')
    search_id = os.getenv('SEARCH_ENGINE_ID')

    query = city + "1920x1080"
    page = 1
    start = (page-1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={search_api_key}&cx={search_id}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = request.request.get(city_url).json()
    count = 1
    search_items = data.get('items')
    image_url = search_items[1]['link']

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Toronto'
        
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}'
    params = {'units': 'metric'}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()

        
        # Check if 'weather' key exists in the response
        if 'weather' in data:
            describe = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            temp = str(data['main']['temp']) + '°C'
        else:
            # If 'weather' key is not present, handle the error
            describe = 'Weather data not available'
            icon = None
            temp = None
        
    except Exception as e:
        # Handle any other exceptions (e.g., network issues)
        describe = 'Error fetching data'
        icon = None
        temp = None

    day = datetime.date.today()
    

    return render(request, 'weather/index.html', {'description': describe, 'icon': icon, 'temp': temp, 'day': day, 'city': city, 'image_url': image_url})
