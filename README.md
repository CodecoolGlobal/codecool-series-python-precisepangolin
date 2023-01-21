# codecool-series
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
*  [Setup](#setup)
*  [Screenshots](#screenshots)
* [Credits](#credits)

## General info
A portal that displays information about a list of shows taken from a database. 

Various parts of the database are displayed on pages listed on the main page, and the data is variously sorted and formatted. In case of the "Filter actors" subpage it is possible to search by genere and actor's name. Occasionally a JavaScript snippet is used, for example on the "Actors" page to display popups. 

## Technologies
* Python version: 3.9
* Flask version: 2.0
* PostgreSQL version: 14.5
* Python-dotenv version: 0.13
* Psycopg2-binary version: 2.9
* Requests version 2.19

## Setup
To run this project in a local development server:
1. Generate the database using /data/data_inserter.py
2. Create a .env file using the .env.template file
3. Run the following commands in the command prompt:
``` 
pip install -r requirements.txt
python3 -m venv venv
venv/Scripts/activate.bat
python3 -m flask --app main run 
```

## Screenshots
![codecool-series](https://user-images.githubusercontent.com/61357898/213877724-258c57be-015d-4838-84a4-9441d9f90bec.png)

## Credits
Credit to Codecool for providing the starter repository and instructions.
