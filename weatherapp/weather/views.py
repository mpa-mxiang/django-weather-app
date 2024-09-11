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

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Toronto'
        
    # URL for weather API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}'
    params = {'units': 'metric'}

    # Query for Google Custom Search
    query = city
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={search_api_key}&cx={search_id}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    # Make the Google Custom Search API request
    city_data = requests.get(city_url).json()

    # Check if the search returned items and retrieve image URL if available
    search_items = city_data.get('items')
    if search_items and len(search_items) > 1:
        image_url = search_items[1]['link']
    else:
        image_url = None  # Handle case where no image is returned

    try:
        # Make the weather API request
        response = requests.get(url, params=params)
        data = response.json()

        # Check if 'weather' key exists in the response
        if 'weather' in data:
            describe = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            temp = str(data['main']['temp']) + '°C'
        else:
            describe = 'Weather data not available'
            icon = None
            temp = None
    except Exception as e:
        # Handle any exceptions (e.g., network issues)
        describe = 'Error fetching data'
        icon = None
        temp = None

    day = datetime.date.today()

    # Render the template with the context
    return render(request, 'weather/index.html', {
        'description': describe,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
        'image_url': image_url
    })
