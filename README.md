# Reverse Geocoding Postgres

## Overview


This project integrates QGIS with ArcGIS and PostgreSQL to capture geographic coordinates from a map, perform reverse geocoding to obtain location names, and save the captured data (latitude, longitude, and location details) into a PostgreSQL database. It allows users to interactively click on a map in QGIS to extract coordinates and store them along with location information in the database.


## Requirements


QGIS (with Python support enabled) 

ArcGIS API for Python

PostgreSQL with Psycopg2 for database connection

Python 3.x

## Installation

1. Install QGIS: Follow the official QGIS installation instructions from QGIS website.

  -> pip install arcgis psycopg2

2. Set up PostgreSQL database:

  -> Ensure you have PostgreSQL installed and running.

  -> Create a database and configure the connection settings in the DB_CONFIG section of the code (dbname, user, password, host, port).

  -> The script will automatically create a table named ndvi_coordinates in the PostgreSQL database if it doesn't already exist.

## Example Output
When you click on the map:

->  Clicked Coordinates: Latitude: 34.0522, Longitude: -118.2437

->  Location: Los Angeles, California, USA

->  Data successfully saved to PostgreSQL.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or issues, please contact csesumit13@gmail.com
