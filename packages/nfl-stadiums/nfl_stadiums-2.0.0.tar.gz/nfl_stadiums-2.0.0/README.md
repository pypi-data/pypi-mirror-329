# NFLTeamStadiums
A simple python package that provides easy access to NFL stadium data such as capacity, location, and weather.

This package utilizes the Wikipedia API to retrieve NFL stadium data, Open-Meteo.com for weather information, 
and provides methods for easy access to the same. Stadium data is fairly static, so by default, this class will save 
the data retrieved from Wikipedia locally for subsequent uses for quicker access and less load on Wikipedia. 
See the below documentation for details on basic usage.

## Installation and Basic Usage
1. Clone or download the repository 
2. Import the class in your code
3. Instantiate the class

```
pip install nfl-stadiums
```

```
from nfl_stadiums import NFLStadiums

# Default instantiation will use local cache if available and print to console
nfl_stadiums = NFLStadiums()

# Set verbose=false to stop printing to console and use_cache=false to retrieve data from wikipedia and overwrite cache
nfl_stadiums = NFLStadiums(use_cache=False, verbose=False)
```
## Methods

### get_stadium_by_team
```
nfl_stadiums.get_stadium_by_team("lions")
```

### get_stadium_by_name
```
nfl_stadiums.get_stadium_by_team("ford field")
```

#### results
```json
{
    "name": "Ford Field",
    "capacity": 65000,
    "imgUrl": "https://en.wikipedia.org/wiki/File:Packers_at_Lions_Dec_2020_(50715608723).jpg",
    "city": "Detroit, Michigan",
    "surface": "FieldTurf CORE",
    "roofType": "Fixed",
    "teams": [
        "Detroit Lions"
    ],
    "yearOpened": 2002,
    "sharedStadium": false,
    "currentTeams": [
        "DET"
    ],
    "coordinates": {
        "lat": 42.34,
        "lon": -83.04555556,
        "primary": "",
        "globe": "earth"
    }
}
```

### calculate_distance_between_stadiums
```
distance_in_miles = nfl_stadiums.calculate_distance_between_stadiums('lions', 'chiefs')
```

### get_weather_forecast_for_stadium
```
# To get the full day
ford_field_weather = nfl_stadiums.get_weather_forecast_for_stadium('lions', '2024-05-30')

# Fine tune with additional parameters, for example, for just gametime
ford_field_weather = nfl_stadiums.get_weather_forecast_for_stadium('lions', '2024-05-30', hour_start=12, hour_end=15, 
                                                                   day_format="%Y-%m-%d",
                                                                   timezone='America/New_York')
```

#### results
```
{
    "latitude": 42.351395, 
    "longitude": -83.06134, 
    "generationtime_ms": 0.10704994201660156, 
    "utc_offset_seconds": -14400, 
    "timezone": "America/New_York", 
    "timezone_abbreviation": "EDT", 
    "elevation": 188.0, 
    "hourly_units": 
        {
            "time": "iso8601", "temperature_2m": "°F", "apparent_temperature": "°F", "precipitation_probability": "%", "precipitation": "inch", "rain": "inch", "showers": "inch", 
            "snowfall": "inch", "snow_depth": "ft", "wind_speed_10m": "mp/h", "wind_speed_80m": "mp/h", "wind_direction_10m": "°"
        }, 
    "hourly": 
        {
            "time": ["2024-05-30T00:00", "2024-05-30T01:00", "2024-05-30T02:00", "2024-05-30T03:00", "2024-05-30T04:00", "2024-05-30T05:00", "2024-05-30T06:00", 
                     "2024-05-30T07:00", "2024-05-30T08:00", "2024-05-30T09:00", "2024-05-30T10:00", "2024-05-30T11:00", "2024-05-30T12:00", "2024-05-30T13:00", 
                     "2024-05-30T14:00", "2024-05-30T15:00", "2024-05-30T16:00", "2024-05-30T17:00", "2024-05-30T18:00", "2024-05-30T19:00", "2024-05-30T20:00", 
                     "2024-05-30T21:00", "2024-05-30T22:00", "2024-05-30T23:00"], 
            "temperature_2m": [50.0, 48.6, 47.3, 46.4, 44.6, 44.4, 43.6, 46.0, 52.3, 57.9, 62.4, 65.8, 67.4, 69.3, 70.6, 72.5, 72.0, 71.1, 70.8, 67.0, 65.3, 61.5, 58.5, 56.0], 
            "apparent_temperature": [44.8, 43.4, 43.0, 42.2, 40.4, 39.7, 40.1, 43.6, 49.1, 53.8, 58.1, 62.2, 65.1, 66.5, 68.5, 69.5, 67.8, 67.2, 65.1, 60.8, 59.9, 57.1, 54.2, 52.0], 
            "precipitation_probability": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            "precipitation": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
            "rain": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
            "showers": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
            "snowfall": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
            "snow_depth": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
            "wind_speed_10m": [4.4, 3.5, 2.2, 1.8, 2.0, 3.5, 1.6, 0.2, 2.3, 4.0, 5.2, 6.7, 7.5, 9.0, 7.8, 9.0, 8.3, 6.3, 5.7, 9.0, 6.5, 4.8, 4.8, 4.8], 
            "wind_speed_80m": [13.5, 11.1, 10.3, 7.9, 6.5, 5.5, 6.2, 7.1, 6.1, 5.5, 7.3, 9.7, 9.4, 11.0, 9.9, 11.1, 9.0, 7.6, 6.8, 11.5, 8.6, 10.5, 11.0, 11.7], 
            "wind_direction_10m": [15, 18, 323, 284, 270, 255, 286, 360, 343, 326, 350, 354, 17, 23, 357, 347, 346, 358, 21, 71, 63, 49, 37, 37]
        }
}
```

### get_stadium_coordinates_by_team
```
self.get_stadium_by_team('jaguars')
```

### get_stadium_coordinates_by_name
```
self.get_stadium_by_name('arrowhead stadium')
```

#### results
```
{'globe': 'earth', 
 'lat': 30.32388889, 
 'lon': -81.6375, 
 'primary': ''
 }
```

### get_list_of_stadium_names
```
nfl_stadiums.get_list_of_stadium_names()
```

#### results
```
['Acrisure Stadium', 'Allegiant Stadium', 'Arrowhead Stadium', 'AT&T Stadium', 'Bank of America Stadium' ...]
```

## Data Source
This package utilizes data from Wikipedia. The core page is 
[here](https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums).

This package utilizes the Open_Meteo.com API found [here](https://open-meteo.com/).


#### You are responsible for how you access and use the data.<br>
Wikipedia content is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. 
For more details on the terms of use, please refer to the 
[Wikimedia Foundation's Terms of Use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use).


See Open-Meteo's terms of use [here](https://open-meteo.com/en/terms).

## License
This project is licensed under the MIT License. See the LICENSE file for details.

