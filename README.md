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
* Main page

![codecool-series](https://user-images.githubusercontent.com/61357898/213877724-258c57be-015d-4838-84a4-9441d9f90bec.png)

Click on the headers below to display animated gif:

<details>
<summary>Show details & actors in show</summary>
<img src="https://user-images.githubusercontent.com/61357898/214286639-4ec2d3b7-02cd-4c9c-8c78-cf6c77abd90b.gif">
</details>

<details>
<summary>Most rated shows</summary>
<img src="https://user-images.githubusercontent.com/61357898/214286688-633f9a05-033f-4cd3-a556-0547f862bcc6.gif">
</details>

<details>
<summary>Actors</summary>
<img src="https://user-images.githubusercontent.com/61357898/214286733-ae57272e-1416-4014-a4bd-1bab8726c8d4.gif">
</details>

<details>
<summary>Filter actors</summary>
<img src="https://user-images.githubusercontent.com/61357898/214286756-1f56a31a-5cc3-41fa-9618-62d1cd27ff83.gif">
</details>

<details>
<summary>Birthday actors</summary>
<img src="https://user-images.githubusercontent.com/61357898/214286769-f2c670cf-0fe0-4085-b8ef-ba7c802f3659.gif">
</details>


## Credits
Credit to Codecool for providing the starter repository and instructions.
