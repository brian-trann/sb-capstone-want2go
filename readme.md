# Want2Go (pending name)

## Goal:
The goal of Want2Go is to provide a more intuitive and 'computationally kind' way discovering new places to eat. The two main features of this application is discovery and keeping track of discovered/matched restaurants. 

## User base:
The target demographic are adults, between 18-35 years old.

## Data:
I plan on using the Google Places API. The API provides all of the necessary information for restaurants, photos, addresses, business hours.

## Approach:
Currently, my database schema only has a Users, Areas, and restaurants table. I may need to add an additional relationship type table, in order to keep the database schema in 3NF or BCNF. I do not foresee any issues with the API I have chosen. The only issues that may come up are from my implementation of this application. The only sensitive information that I will need to store is the password. 


## Initial Schema Design:
### users table
|    | user_account |   | 
|----|--------------|---| 
| PK | id           |   | 
|    | name         |   | 
|    | email        |   | 
|    | password     |   | 
| FK | likes_id     |   | 
| FK | dislikes_id  |   | 
| FK | areas_id     |   |

### likes
|    | likes          |   |
|----|----------------|---|
| PK | id             |   |
| FK | user_id        |   |
| FK | restaurant_id  |   |

### dislikes
|    | dislikes       |   |
|----|----------------|---|
| PK | id             |   |
| FK | user_id        |   |
| FK | restaurant_id  |   |

### areas
|    | area    |   |
|----|---------|---|
| PK | id      |   |
|    | zipcode |   |
|    | city    |   |
| FK | user_id |   |

### restaurants
|    | restaurants       |   |
|----|-------------------|---|
| PK | id                |   |
|    | name              |   |
|    | address           |   |
|    | city              |   |
|    | state             |   |
|    | description       |   |
|    | google_place_id   |   |
|    | fetched_timestamp |   |


## User Flow & Sequence Diagrams:

* Basic user flows are in /assets 
  * Does not include:
    * Account settings
    * "Areas" tab

## Future goals:
* additional toggle switches for users to specify restaurant search: corporate/non corporate, open now, etc.
* React native/ Mobile functionality (with swiping)