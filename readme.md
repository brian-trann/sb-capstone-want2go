# Want2Go (pending name)

## Goal:
The goal of Want2Go is to provide a more intuitive and 'computationally kind' way discovering new places to eat. The two main features of this application is discovery and keeping track of discovered/matched restaurants. 

## User base:
The target demographic are adults, between 18-35 years old.

## Data:
I plan on using the Yelp Fusion API. The API provides all of the necessary information for restaurants, photos, addresses, business hours.

## Approach:
Currently, my database schema only has a Users, Areas, and restaurants table. I may need to add an additional relationship type table, in order to keep the database schema in 3NF or BCNF. I do not foresee any issues with the API I have chosen. The only issues that may come up are from my implementation of this application. The only sensitive information that I will need to store is the password. 


## Initial Schema Design:
### user_accounts table
|    | user_account |   | 
|----|--------------|---| 
| PK | id           |   | 
|    | name         |   | 
|    | email        |   | 

### interested_in_relation table
|        | interested_in_relation |   |
|--------|------------------------|---|
| PK,FK1 | user_account_id        |   |
| PK,FK2 | restaurant_id          |   |
|        | area_id                |   |
|        | relation_type          |   |

### restaurants table
|    | restaurant |   |
|----|------------|---|
| PK | id         |   |
|    | name       |   |

### areas table
|    | area    |   |
|----|---------|---|
| PK | id      |   |
|    | zipcode?|   |

## User Flow:

* Log In/ Create account
* Restaurant
* Restaurant - detailed
* Likes
* Dislikes
* Areas
* Settings

## Future goals:
* additional toggle switches for users to specify restaurant search: corporate/non corporate, open now, etc.
* React native/ Mobile functionality (with swiping)