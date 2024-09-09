from django.shortcuts import render

# Create your views here.
def home(request):
    api_key = os.getenv('OPEN_WEATHER_API_KEY')  # Grab the API key from environment variables
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'New York'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    PARMAS = {'units': 'metric'}
    return render(request, 'weather/index.html')