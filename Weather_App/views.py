from django.shortcuts import render
import requests, datetime

# Create your views here.
def homeFun(request):
    # Get the city from the POST request, or default to 'Ahmedabad'
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Ahmedabad'
    
    # OpenWeatherMap API URL with city and API key
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=d0a509ed97fa0a83910e6e812bb38a8e'
    PARAMS = {'units': 'metric'}
    
    try:
        # Use `requests.get()` to make the API call
        response = requests.get(url, params=PARAMS)
        data = response.json()
        
        # Check if the API response contains 'weather' key
        if 'weather' in data:
            # Extract data from the API response
            description = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            temp = data['main']['temp']
        else:
            # If 'weather' key is not in response, show custom error message
            return render(request, 'Weather_App/404.html', {'error_message': f"City '{city}' not found. Please enter a valid city name."})
        
        # Get the current date
        day = datetime.date.today()
        
        # Prepare the context for the template
        context = {
            'city': city,
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day
        }
        
    except requests.exceptions.RequestException as e:
        # Handle API request errors (network issues, etc.)
        return render(request, 'Weather_App/404.html', {'error_message': "Failed to fetch data from weather API. Please try again later."})
    
    # Render the template with the context data
    return render(request, 'Weather_App/home.html', context)
