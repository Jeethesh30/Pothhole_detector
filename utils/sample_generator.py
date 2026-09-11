"""
Bengaluru Sample Data & Route Coordinate Generator
"""

import os
import cv2
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data")
IMAGE_DIR = os.path.join(SAMPLE_DIR, "images")

# Key Bengaluru Routes (Coordinates: Lat, Lon, Location Name, IsHazard, Severity, DistanceFromStart)
BENGALURU_ROUTES = {
    "Outer Ring Road (Silk Board -> Marathahalli)": [
        {"lat": 12.9172, "lon": 77.6228, "name": "Silk Board Junction", "hazard": False, "severity": None, "dist": 0},
        {"lat": 12.9116, "lon": 77.6389, "name": "HSR Layout Flyover", "hazard": True, "severity": "Moderate", "dist": 1.8},
        {"lat": 12.9255, "lon": 77.6835, "name": "Agara Lake Junction", "hazard": False, "severity": None, "dist": 3.5},
        {"lat": 12.9279, "lon": 77.6800, "name": "Iblur Signal", "hazard": True, "severity": "Severe", "dist": 4.2},
        {"lat": 12.9366, "lon": 77.6963, "name": "Bellandur EcoSpace", "hazard": True, "severity": "Severe", "dist": 6.1},
        {"lat": 12.9430, "lon": 77.6970, "name": "Devarabeesanahalli Flyover", "hazard": True, "severity": "Moderate", "dist": 7.3},
        {"lat": 12.9515, "lon": 77.6997, "name": "Kadubeesanahalli", "hazard": False, "severity": None, "dist": 8.5},
        {"lat": 12.9568, "lon": 77.7011, "name": "Marathahalli Bridge", "hazard": True, "severity": "Severe", "dist": 9.8},
    ],
    "Koramangala -> Indiranagar Corridor": [
        {"lat": 12.9345, "lon": 77.6265, "name": "Koramangala Sony World Signal", "hazard": True, "severity": "Moderate", "dist": 0},
        {"lat": 12.9382, "lon": 77.6305, "name": "Koramangala 80ft Road", "hazard": False, "severity": None, "dist": 1.2},
        {"lat": 12.9550, "lon": 77.6410, "name": "Domlur Flyover", "hazard": True, "severity": "Severe", "dist": 3.4},
        {"lat": 12.9620, "lon": 77.6430, "name": "Command Hospital", "hazard": False, "severity": None, "dist": 4.5},
        {"lat": 12.9719, "lon": 77.6412, "name": "Indiranagar 100ft Road", "hazard": True, "severity": "Minor", "dist": 5.8},
        {"lat": 12.9784, "lon": 77.6408, "name": "Indiranagar Metro Station", "hazard": False, "severity": None, "dist": 6.7},
    ],
    "Whitefield Tech Belt (Hoodi -> ITPL)": [
        {"lat": 12.9918, "lon": 77.7161, "name": "Hoodi Junction", "hazard": True, "severity": "Severe", "dist": 0},
        {"lat": 12.9863, "lon": 77.7289, "name": "Vydehi Hospital Circle", "hazard": True, "severity": "Moderate", "dist": 1.9},
        {"lat": 12.9847, "lon": 77.7377, "name": "ITPL Main Gate", "hazard": False, "severity": None, "dist": 3.1},
        {"lat": 12.9778, "lon": 77.7471, "name": "Hope Farm Circle", "hazard": True, "severity": "Severe", "dist": 4.8},
    ],
    "Airport Expressway (Hebbal -> Yelahanka)": [
        {"lat": 13.0358, "lon": 77.5970, "name": "Hebbal Flyover", "hazard": True, "severity": "Moderate", "dist": 0},
        {"lat": 13.0645, "lon": 77.5950, "name": "Kodigehalli Gate", "hazard": False, "severity": None, "dist": 3.2},
        {"lat": 13.0825, "lon": 77.5930, "name": "Jakkur Aerodrome", "hazard": True, "severity": "Minor", "dist": 5.4},
        {"lat": 13.1007, "lon": 77.5963, "name": "Yelahanka Bypass", "hazard": False, "severity": None, "dist": 7.8},
    ]
}

def ensure_sample_directories():
    os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_synthetic_road_images():
    """Generates synthetic asphalt road images with realistic pothole defects for demo/testing."""
    ensure_sample_directories()
    
    sample_files = []
    configs = [
        {"filename": "bengaluru_orr_severe.jpg", "defects": [((320, 260), (90, 60), "Severe"), ((180, 310), (45, 30), "Moderate")]},
        {"filename": "koramangala_pothole_1.jpg", "defects": [((400, 300), (120, 80), "Severe")]},
        {"filename": "whitefield_road_defect.jpg", "defects": [((220, 250), (60, 40), "Moderate"), ((480, 320), (70, 50), "Minor")]},
        {"filename": "clean_road_sample.jpg", "defects": []}
    ]

    for cfg in configs:
        file_path = os.path.join(IMAGE_DIR, cfg["filename"])
        if not os.path.exists(file_path):
            # Create synthetic asphalt road texture
            h, w = 480, 640
            # Base asphalt dark grey color
            img = np.full((h, w, 3), (60, 62, 65), dtype=np.uint8)
            
            # Add subtle road texture noise
            noise = np.random.randint(-15, 15, (h, w, 3), dtype=np.int16)
            img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            
            # Draw yellow lane lines
            cv2.line(img, (w//2, h), (w//2 - 40, h//2), (0, 215, 255), 4)
            cv2.line(img, (w//2, h//2 - 20), (w//2 - 60, h//4), (0, 215, 255), 4)

            # Draw synthetic pothole cracks/holes
            for center, axes, sev in cfg["defects"]:
                # Pothole dark cavity
                cv2.ellipse(img, center, axes, random.randint(-15, 15), 0, 360, (25, 25, 28), -1)
                # Outer rough edge
                cv2.ellipse(img, center, (axes[0]+8, axes[1]+6), random.randint(-15, 15), 0, 360, (40, 42, 45), 3)
                # Inner shadow/depth
                cv2.ellipse(img, (center[0]-5, center[1]-4), (axes[0]-10, axes[1]-8), random.randint(-15, 15), 0, 360, (12, 12, 15), -1)
                
            cv2.imwrite(file_path, img)
        sample_files.append(file_path)

    return sample_files

def get_sample_hazard_dataframe(count=60):
    """Generates realistic historical Bengaluru road hazard data for Spatial Analytics & Heatmap."""
    np.random.seed(42)
    zones = [
        {"name": "Outer Ring Road - Bellandur", "lat": 12.9366, "lon": 77.6963, "ward": "Ward 150 (Bellandur)"},
        {"name": "Koramangala 80ft Road", "lat": 12.9345, "lon": 77.6265, "ward": "Ward 151 (Koramangala)"},
        {"name": "Indiranagar 100ft Road", "lat": 12.9719, "lon": 77.6412, "ward": "Ward 110 (Indiranagar)"},
        {"name": "Whitefield ITPL Road", "lat": 12.9847, "lon": 77.7377, "ward": "Ward 84 (Hagadur)"},
        {"name": "Hebbal Flyover Junction", "lat": 13.0358, "lon": 77.5970, "ward": "Ward 8 (Hebbal)"},
        {"name": "Silk Board Junction", "lat": 12.9172, "lon": 77.6228, "ward": "Ward 174 (HSR Layout)"},
        {"name": "Marathahalli Bridge", "lat": 12.9568, "lon": 77.7011, "ward": "Ward 85 (Doddanekkundi)"},
        {"name": "Old Airport Road", "lat": 12.9550, "lon": 77.6410, "ward": "Ward 112 (Domlur)"}
    ]

    severities = ["Severe", "Moderate", "Minor"]
    weights = [0.4, 0.4, 0.2]

    data = []
    base_time = datetime.now() - timedelta(days=14)

    for i in range(count):
        z = random.choice(zones)
        # Random jitter around zone coordinate (~300m)
        lat = z["lat"] + random.uniform(-0.008, 0.008)
        lon = z["lon"] + random.uniform(-0.008, 0.008)
        sev = random.choices(severities, weights=weights)[0]
        
        depth_cm = round(random.uniform(8.0, 22.0) if sev == "Severe" else (random.uniform(4.0, 8.0) if sev == "Moderate" else random.uniform(1.5, 4.0)), 1)
        area_sqm = round(random.uniform(0.5, 2.2) if sev == "Severe" else (random.uniform(0.2, 0.5) if sev == "Moderate" else random.uniform(0.05, 0.2)), 2)
        confidence = round(random.uniform(0.82, 0.98), 2)
        
        reported_date = base_time + timedelta(hours=random.randint(1, 336))

        data.append({
            "Hazard ID": f"BLR-HAZ-{1000 + i}",
            "Location Name": z["name"],
            "Ward": z["ward"],
            "Latitude": round(lat, 5),
            "Longitude": round(lon, 5),
            "Severity": sev,
            "Est. Depth (cm)": depth_cm,
            "Est. Surface Area (m²)": area_sqm,
            "Confidence": confidence,
            "Status": random.choice(["Unrepaired - High Priority", "Inspected", "Scheduled for BBMP Repair"]),
            "Reported Time": reported_date.strftime("%Y-%m-%d %H:%M")
        })

    return pd.DataFrame(data)
