from .data import countries_data

def get_country_info(country_name):
    for country in countries_data:
        if country['name'].lower() == country_name.lower():
            return country
    return None

def get_all_countries():
    return countries_data
