from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import Qt
from arcgis.geocoding import reverse_geocode
from arcgis.gis import GIS
import psycopg2

# Initialize ArcGIS GIS connection
gis = GIS()  # Anonymous connection

# PostgreSQL connection details
DB_CONFIG = {
    "dbname": "abc",
    "user": "abc",
    "password": "abc",
    "host": "localhost",
    "port": "1234"
}

# Function to create the table if it doesn't exist
def create_table():
    """
    Create the PostgreSQL table if it does not exist.
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ndvi_coordinates (
                        id SERIAL PRIMARY KEY,
                        latitude DOUBLE PRECISION NOT NULL,
                        longitude DOUBLE PRECISION NOT NULL,
                        location_details VARCHAR(255)
                    )
                    """
                )
                print("Table 'ndvi_coordinates' is ready.")
    except Exception as e:
        print(f"Error creating table: {str(e)}")

# Function to perform reverse geocoding using ArcGIS API
def arcgis_reverse_geocode(lat, lon):
    """
    Get location name from latitude and longitude using ArcGIS reverse_geocode.
    """
    try:
        location = reverse_geocode({"x": lon, "y": lat, "spatialReference": {"wkid": 4326}})
        if "address" in location:
            return location["address"]["LongLabel"]
        else:
            return "No address found"
    except Exception as e:
        print(f"Error performing reverse geocoding: {str(e)}")
        return "Unknown location"

# Function to save data into PostgreSQL
def save_to_postgres(lat, lon, location_details):
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Check for duplicates
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM ndvi_coordinates
                    WHERE latitude = %s AND longitude = %s
                    """,
                    (lat, lon)
                )
                if cursor.fetchone()[0] > 0:
                    print("Duplicate entry. Data not saved.")
                    return
                
                # Insert data into the table
                cursor.execute(
                    """
                    INSERT INTO ndvi_coordinates (latitude, longitude, location_details)
                    VALUES (%s, %s, %s)
                    """,
                    (lat, lon, location_details)
                )
                print("Data successfully saved to PostgreSQL.")
    except Exception as e:
        print(f"Error saving to PostgreSQL: {str(e)}")

# Map tool class to capture mouse clicks
class MapClickTool(QgsMapTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas

    def canvasReleaseEvent(self, event):
        """
        Triggered when the mouse is clicked on the map.
        """
        try:
            # Get the clicked point in map coordinates
            point = self.toMapCoordinates(event.pos())
            
            # Get the active raster layer
            raster_layer = iface.activeLayer()
            if raster_layer is None or not isinstance(raster_layer, QgsRasterLayer):
                print("No active raster layer found or the active layer is not a raster.")
                return

            # Transform the point to WGS84 if necessary
            if not raster_layer.crs().isGeographic():
                transform = QgsCoordinateTransform(
                    self.canvas.mapSettings().destinationCrs(),
                    QgsCoordinateReferenceSystem("EPSG:4326"),
                    QgsProject.instance()
                )
                point = transform.transform(point)

            lat, lon = point.y(), point.x()
            print(f"Clicked Coordinates: Latitude: {lat}, Longitude: {lon}")

            # Perform reverse geocoding
            location_name = arcgis_reverse_geocode(lat, lon)
            print(f"Location: {location_name}")

            # Save data to PostgreSQL
            save_to_postgres(lat, lon, location_name)

        except Exception as e:
            print(f"Error in NDVICoordinates: {str(e)}")

# Activate the map click tool
def activate_map_click_tool():
    """
    Activates the custom map click tool.
    """
    try:
        # Ensure the database table exists
        create_table()

        # Activate the map tool
        canvas = iface.mapCanvas()
        tool = MapClickTool(canvas)
        canvas.setMapTool(tool)
        print("Map click tool activated. Click on the map to get location details and save them to PostgreSQL.")
    except Exception as e:
        print(f"Error activating map click tool: {str(e)}")

# Activate the tool
activate_map_click_tool()
