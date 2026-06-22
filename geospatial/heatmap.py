import folium
from folium.plugins import HeatMap
import random

def generate_heatmap():
    # Fraud hotspot data for Indian cities (lat, lon, intensity)
    fraud_data = [
        # Delhi NCR cluster
        [28.6139, 77.2090, 0.9], [28.6300, 77.2200, 0.85], [28.5800, 77.1900, 0.8],
        [28.6500, 77.2500, 0.75], [28.7000, 77.1500, 0.7], [28.6200, 77.3000, 0.65],
        [28.5500, 77.2700, 0.8], [28.6800, 77.0800, 0.6],

        # Mumbai cluster
        [19.0760, 72.8777, 0.88], [19.1000, 72.9000, 0.82], [18.9400, 72.8300, 0.77],
        [19.2000, 72.9800, 0.7], [19.0500, 72.8400, 0.85], [18.9800, 72.8100, 0.6],

        # Bangalore cluster
        [12.9716, 77.5946, 0.82], [12.9900, 77.6100, 0.75], [12.9400, 77.5700, 0.7],
        [13.0200, 77.5500, 0.65], [12.9600, 77.6400, 0.78],

        # Hyderabad
        [17.3850, 78.4867, 0.72], [17.4100, 78.5000, 0.68], [17.3600, 78.4600, 0.65],

        # Chennai
        [13.0827, 80.2707, 0.7], [13.1000, 80.2900, 0.65], [13.0600, 80.2500, 0.6],

        # Kolkata
        [22.5726, 88.3639, 0.68], [22.5900, 88.3800, 0.63], [22.5500, 88.3400, 0.6],

        # Ahmedabad
        [23.0225, 72.5714, 0.65], [23.0400, 72.5900, 0.6],

        # Pune
        [18.5204, 73.8567, 0.63], [18.5400, 73.8700, 0.58],

        # Jaipur
        [26.9124, 75.7873, 0.6], [26.9300, 75.8100, 0.55],

        # Lucknow
        [26.8467, 80.9462, 0.62], [26.8600, 80.9600, 0.57],
    ]

    # Create map centered on India
    m = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=5,
        tiles="CartoDB dark_matter"
    )

    # Add heatmap layer
    HeatMap(
        fraud_data,
        radius=30,
        blur=20,
        max_zoom=10,
        gradient={0.2: "blue", 0.4: "cyan", 0.6: "yellow", 0.8: "orange", 1.0: "red"}
    ).add_to(m)

    # Add city markers with fraud stats
    city_stats = [
        {"city": "Delhi NCR", "lat": 28.6139, "lon": 77.2090,
         "cases": 12450, "type": "Digital Arrest, KYC Scam", "color": "red"},
        {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777,
         "cases": 9870, "type": "Investment Fraud, UPI Scam", "color": "red"},
        {"city": "Bangalore", "lat": 12.9716, "lon": 77.5946,
         "cases": 7650, "type": "Job Fraud, Tech Support Scam", "color": "orange"},
        {"city": "Hyderabad", "lat": 17.3850, "lon": 78.4867,
         "cases": 5430, "type": "Lottery Scam, Phishing", "color": "orange"},
        {"city": "Chennai", "lat": 13.0827, "lon": 80.2707,
         "cases": 4320, "type": "Bank Freeze Scam", "color": "orange"},
        {"city": "Kolkata", "lat": 22.5726, "lon": 88.3639,
         "cases": 3980, "type": "Electricity Scam, Digital Arrest", "color": "orange"},
        {"city": "Ahmedabad", "lat": 23.0225, "lon": 72.5714,
         "cases": 3210, "type": "FedEx Courier Scam", "color": "yellow"},
        {"city": "Pune", "lat": 18.5204, "lon": 73.8567,
         "cases": 2870, "type": "Investment Fraud", "color": "yellow"},
    ]

    for stat in city_stats:
        folium.CircleMarker(
            location=[stat["lat"], stat["lon"]],
            radius=10,
            color=stat["color"],
            fill=True,
            fill_opacity=0.8,
            popup=folium.Popup(
                f"""
                <div style='font-family:Arial; min-width:180px'>
                    <b style='color:#e74c3c'>🚨 {stat['city']}</b><br>
                    <b>Reported Cases:</b> {stat['cases']:,}<br>
                    <b>Top Scam Types:</b><br>{stat['type']}
                </div>
                """,
                max_width=250
            ),
            tooltip=f"{stat['city']}: {stat['cases']:,} cases"
        ).add_to(m)

    # Add legend
    legend_html = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
                background-color: rgba(0,0,0,0.8); padding: 12px 16px;
                border-radius: 8px; color: white; font-family: Arial; font-size: 13px;">
        <b>🗺️ Fraud Intensity</b><br>
        <span style="color:#ff4444">●</span> Critical (10,000+ cases)<br>
        <span style="color:#ff8800">●</span> High (5,000–10,000 cases)<br>
        <span style="color:#ffff00">●</span> Medium (1,000–5,000 cases)<br>
        <span style="color:#00aaff">●</span> Low (&lt;1,000 cases)
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m