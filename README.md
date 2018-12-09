# SendIt [![Build Status](https://travis-ci.org/PatrickMugayaJoel/SendIt.svg?branch=develop)](https://travis-ci.org/PatrickMugayaJoel/SendIt) [![Coverage Status](https://coveralls.io/repos/github/PatrickMugayaJoel/SendIt/badge.svg?branch=develop)](https://coveralls.io/github/PatrickMugayaJoel/SendIt?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/7a64cecee106d76232d1/maintainability)](https://codeclimate.com/github/PatrickMugayaJoel/SendIt/maintainability)

SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight & size.
    

# Getting Started

For installation of this project:  `$ https://github.com/PatrickMugayaJoel/SendIt.git`

# Prerequisites

* A text editor e.g. Sublime Text, Notepad++
* A python runtime enviroment
* A web browser e.g. Google Chrome, Mozilla Firefox

# Features

* Users can signup.
* Users can login.
* Users can add a parcel.
* Users can view all his parcels.
* Admin can update the status of a delivery order.
 
# Languages

* PYTHON 3.7
 
# Installing

* Clone this: https://github.com/PatrickMugayaJoel/SendIt/tree/feature
* Install python 3.7
* Setup a virtual enviroment and activate it
* Install requirements
* Execute the 'run.py' file in the root directory.

## Login Credentials

| User Role | Username | Password |
| ----------- | -------- | --------- |
| Owner | admin | admin |

## Endpoints

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| POST | /api/v1/signup |Create a New User|
| POST | /api/v1/login |Login a User|
| POST | /api/v1/parcels | Adds a new parcel |
| GET | /api/v1/parcels | list of parcel |
| GET | /api/v1/parcels/1 | Get a parcel |
| PUT | /api/v1/parcels/1/cancel | Cancel a parcel |
| PUT | /api/v1/parcels/1/update | Update a parcel |
| PUT | /api/v1/users/1/promote | Makes user an admin |
| GET | /api/v1/users/1/parcels | User's parcels |
| GET | /api/v1/users | List of users |
| GET | /api/v1/users/1 | Returns a user |

## Run the app

`$ python run.py`

## Authors

* **Mugaya Joel Patrick**
 
## Acknowledgments

* Andela





