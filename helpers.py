import zipcodes
import requests

def place_search_request(latitude:str,longitude:str,key:str):
    '''place_search_request() sends a GET request to the Google Place Search API
    Parameters:
        latitude : user's city's latitude
        longitude : user's city's longitude 
        key : PRIVATE_API_KEY

    Returns dictionary:
        place_ids : array of place_ids
        next_page_token : token  #TODO look up documentation on how to use this.


    #TODO insert the following code below to use new data. Currently useing old data
    ### NOTE I CHANGED THE json keys to be lowerCamelCase
    # response = requests.get(url).json()
    # results = response['results'] 
    # next_page_token = response['next_page_token']
    # place_ids = [item['place_id'] for item in results]
    # return {"place_ids":place_ids,"next_page_token":next_page_token}
    '''
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants&location={latitude},{longitude}&radius=10000&key={key}"


    OLD_DICT_RESPONSE = {'placeIds': ['ChIJ_3Ksr2x344kRvwN5KyrNiMc', 'ChIJv7N3hSV_44kRkbRW_O8BtzI', 'ChIJ_Wz5mxx344kRSmUKSAw6bz0', 'ChIJI5Ohj0J344kRDC2E6zMzvNk', 'ChIJTRa97T9344kRt_HspVyvshg', 'ChIJFRuPfQt644kR3soGgGtqgY8', 'ChIJ8XZQ9A5644kR-8i3134hx2I', 'ChIJR0jyIuxw44kRaaA2TCmdnmk', 'ChIJ4-dkqBSc44kR20hvO_9FFzc', 'ChIJ5QEBOHB344kRYHtXCUi_EiE', 'ChIJ57pOLgV644kR7DyFbT5fANk', 'ChIJ52vRLHR644kRjaD_7vUhhFY', 'ChIJRzsVPRB644kR6p7R8VYa4gs', 'ChIJSWC59taC44kRrgJ2CnEY2Kw', 'ChIJ5VK6SUh344kRL0BQ8IHUU6A', 'ChIJD1bhcBV644kR2bOt1la-nKk', 'ChIJTbj3DvF544kRB0odgAGKVPo', 'ChIJm0LFxvV544kR6CAUr4kduZU', 'ChIJZ4d2mY1544kRMVkt11DkMJg', 'ChIJ42aIcDJ444kRGLDj7pEzEoc'], 'nextPageToken': 'ATtYBwLqxgc886p770KWGpFbXWzx4gZELM6jm1JEDwkJ4ojkPksl9MuXuEFUg69RgQpdYnGEg-rkW2gfC4Fpieya9pUCBz33aqSUSB_Qt8ogg5B2WlfPlMbXfFH4iQZPoWVjgRZdQM_o6xP2Xe9Drn3LzuDgdRmBdLC1aUalSadHOEw0JStOA9lelXZDj-qnkMkvu9Q9T06SByxawm8eoEKSg7qvC3aP8NPndUqkyWEaXfVSU8lQ0MhJs-5eaD46raXBw2Ye1J-XNCe_QyFIS7dFYMJxAtznfRdrqYCgz2XFHHsmk806GJUd2U4uCb80xeqxzSsct5n0MNneIMye1V4CbdguGCGP8Ne4LYT5STc_r3VJlgyVKR2W1R-KJm0GCTeKUYjKF-BNHkoJmTmi66AcNouhL2Ps2QQ3_MbS6lB6V8qejjN-TNKFI2KZ_PlKd5sXD4vR'}
    return OLD_DICT_RESPONSE