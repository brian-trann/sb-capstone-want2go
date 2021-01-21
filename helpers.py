import zipcodes
import requests
from secrets import PRIVATE_API_KEY

def place_search_request(latitude:str,longitude:str,key=PRIVATE_API_KEY):
    '''place_search_request() sends a GET request to the Google Place Search API
    Parameters:
        latitude : user's city's latitude
        longitude : user's city's longitude 
        key : PRIVATE_API_KEY

    Returns dictionary:
        place_ids : array of place_ids
        next_page_token : token 
    '''
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants&location={latitude},{longitude}&radius=20000&key={key}"

    response = requests.get(url).json()
    results = response['results'] 
    next_page_token = response['next_page_token']
    place_ids = [item['place_id'] for item in results]
    return {"place_ids":place_ids,"next_page_token":next_page_token}


def google_details_request(place_id:str,key=PRIVATE_API_KEY):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?key={key}&place_id={place_id}"
    response = requests.get(url).json()
    # print(response)
    status = response['status']
    name = response['result']['name']
    address = response['result']['formatted_address']
    google_place_id = response['result']['place_id']
    photos = response['result']['photos']

    photo_references = [photo['photo_reference'] for photo in photos]

    data = {"status":status, 
                "details":{
                    "google_place_id":google_place_id,
                    "name":name,
                    "address":address,
                    "photo_references":photo_references
                    }}
   
    return data

def google_photo_request(photo_reference:str, key=PRIVATE_API_KEY, maxwidth=700):
    """Makes a request to the Google Photos API. Returns a blob """
    url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={maxwidth}&photo_reference={photo_reference}&key={key}"
    response = requests.get(url)
    data = {"url":response.url}
    return data

def google_next_page(pagetoken: str, key=PRIVATE_API_KEY):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={pagetoken}&key={key}"
    response = requests.get(url).json()
    results = response['results'] 
    next_page_token = response['next_page_token']
    place_ids = [item['place_id'] for item in results]
    return {"place_ids":place_ids,"next_page_token":next_page_token}