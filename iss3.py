import requests
import json
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def fetch_iss_data():
    url = "https://iss-mimic.github.io/Mimic/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Since the page might not directly return JSON, adapt parsing here if necessary
        # Assuming the relevant data is within a specific JSON-like endpoint or embedded
        data = extract_data_from_html(response.text)
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def extract_data_from_html(html_content):
    """
    Parse the HTML content to extract relevant ISS data.
    Adjust this function based on the structure of the webpage.
    """
    # For this example, mock some extracted data since parsing isn't implemented
    # In production, use libraries like BeautifulSoup or regex for accurate parsing.
    return {
        "location": {
            "latitude": 51.509865,
            "longitude": -0.118092,
            "altitude": 408.0
        },
        "velocity": 27600,
        "timestamp": "2025-01-01T12:00:00Z",
        "urine_tank": "50%",
        "waste_water_tank": "30%",
        "air_pressure": "101.3 kPa",
        "station_mode": "Normal"
    }

def display_iss_data(data):
    console = Console()

    if "error" in data:
        console.print(f"[bold red]Error fetching ISS data:[/bold red] {data['error']}")
        return

    table = Table(title="[bold blue]International Space Station (ISS) Data[/bold blue]")

    table.add_column("Property", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    location = data.get("location", {})
    table.add_row("Latitude", str(location.get("latitude", "N/A")))
    table.add_row("Longitude", str(location.get("longitude", "N/A")))
    table.add_row("Altitude (km)", str(location.get("altitude", "N/A")))
    table.add_row("Velocity (km/h)", str(data.get("velocity", "N/A")))
    table.add_row("Urine Tank", data.get("urine_tank", "N/A"))
    table.add_row("Waste Water Tank", data.get("waste_water_tank", "N/A"))
    table.add_row("Air Pressure", data.get("air_pressure", "N/A"))
    table.add_row("Station Mode", data.get("station_mode", "N/A"))
    table.add_row("Timestamp", data.get("timestamp", "N/A"))

    console.print(table)
    display_iss_position_on_globe(data)

def display_iss_position_on_globe(data):
    location = data.get("location", {})
    if not location:
        print("No location data available to plot.")
        return

    lat = location.get("latitude")
    lon = location.get("longitude")

    if lat is None or lon is None:
        print("Incomplete location data.")
        return

    # Set up the map
    fig = plt.figure(figsize=(10, 7))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=lon, central_latitude=lat))

    # Add a stock image background
    ax.stock_img()

    # Add features to the map
    ax.add_feature(cfeature.LAND, color='lightgray')
    ax.add_feature(cfeature.OCEAN, color='aqua')
    ax.add_feature(cfeature.COASTLINE, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Plot the ISS position
    ax.plot(lon, lat, marker='o', color='red', markersize=10, transform=ccrs.Geodetic(), label='ISS Position')

    # Add data text to the map
    plt.text(
        0.5, -0.1, 
        f"Velocity: {data.get('velocity', 'N/A')} km/h\n"
        f"Air Pressure: {data.get('air_pressure', 'N/A')}\n"
        f"Urine Tank: {data.get('urine_tank', 'N/A')}\n"
        f"Waste Water Tank: {data.get('waste_water_tank', 'N/A')}\n"
        f"Station Mode: {data.get('station_mode', 'N/A')}",
        horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes,
        fontsize=10,
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
    )

    plt.legend(loc='lower left')
    plt.title("ISS Current Position")
    plt.show()

def main():
    iss_data = fetch_iss_data()
    display_iss_data(iss_data)

if __name__ == "__main__":
    main()

