"""
Vehicle Telemetry & Predictive Navigation Warning Engine
"""

import math
import random
import numpy as np
from utils.sample_generator import BENGALURU_ROUTES

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates distance in meters between two lat/lon points."""
    R = 6371000  # Radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class VehicleTelemetrySimulator:
    def __init__(self, route_name=None):
        self.set_route(route_name)

    def set_route(self, route_name):
        routes = list(BENGALURU_ROUTES.keys())
        if not route_name or route_name not in BENGALURU_ROUTES:
            self.route_name = routes[0]
        else:
            self.route_name = route_name
        self.waypoints = BENGALURU_ROUTES[self.route_name]

    def get_telemetry_step(self, step_idx):
        """
        Given a step_idx (0 to 100 loop index), returns:
        - current_lat, current_lon
        - current_location_name
        - current_speed (km/h)
        - vibration_z_gforce
        - proactive_precaution: Dict with warning details if an upcoming hazard is detected within 150m
        - is_hitting_pothole: Bool
        """
        num_waypoints = len(self.waypoints)
        if num_waypoints < 2:
            return {}

        # Map step index to continuous fractional waypoint position
        total_segments = num_waypoints - 1
        pos_continuous = (step_idx % 100) / 100.0 * total_segments
        
        seg_idx = int(pos_continuous)
        seg_fraction = pos_continuous - seg_idx
        
        if seg_idx >= total_segments:
            seg_idx = total_segments - 1
            seg_fraction = 1.0

        p1 = self.waypoints[seg_idx]
        p2 = self.waypoints[min(seg_idx + 1, total_segments)]

        # Linear interpolation between waypoints
        curr_lat = p1["lat"] + (p2["lat"] - p1["lat"]) * seg_fraction
        curr_lon = p1["lon"] + (p2["lon"] - p1["lon"]) * seg_fraction
        
        location_name = p1["name"] if seg_fraction < 0.5 else p2["name"]

        # Look ahead for upcoming hazards along the route
        proactive_precaution = None
        upcoming_hazard = None
        min_dist_m = 999999

        for wp in self.waypoints:
            if wp.get("hazard"):
                dist = calculate_haversine_distance(curr_lat, curr_lon, wp["lat"], wp["lon"])
                if dist < min_dist_m:
                    min_dist_m = dist
                    upcoming_hazard = wp

        # Trigger Precautionary Warning if upcoming hazard is within 180 meters
        is_hitting_pothole = False
        vibration_g = round(random.uniform(0.85, 1.15), 2)
        base_speed = random.randint(42, 54)

        if upcoming_hazard:
            if min_dist_m <= 25:
                # Vehicle is currently hitting/passing the pothole!
                is_hitting_pothole = True
                sev = upcoming_hazard["severity"]
                vibration_g = round(random.uniform(3.2, 4.8) if sev == "Severe" else random.uniform(2.1, 3.1), 2)
                base_speed = random.randint(15, 25) # Reduced speed on impact
                
                proactive_precaution = {
                    "active": True,
                    "status": "IMPACT ZONE",
                    "distance_m": int(min_dist_m),
                    "hazard_name": upcoming_hazard["name"],
                    "severity": upcoming_hazard["severity"],
                    "recommended_speed": "15 km/h",
                    "message": f"⚠️ HAZARD IMPACT: Passing {upcoming_hazard['severity']} pothole at {upcoming_hazard['name']}! Vibration shock: {vibration_g}g"
                }

            elif min_dist_m <= 180:
                # Proactive warning window ahead!
                sev = upcoming_hazard["severity"]
                target_rec_speed = "20 km/h" if sev == "Severe" else "30 km/h"
                base_speed = max(18, int(base_speed - ((180 - min_dist_m) / 180.0) * 25))
                
                proactive_precaution = {
                    "active": True,
                    "status": "PROACTIVE PRECAUTION",
                    "distance_m": int(min_dist_m),
                    "hazard_name": upcoming_hazard["name"],
                    "severity": upcoming_hazard["severity"],
                    "recommended_speed": target_rec_speed,
                    "message": f"🚨 PRECAUTION: {sev} Road Hazard detected {int(min_dist_m)}m ahead near {upcoming_hazard['name']}! Slow down to {target_rec_speed}."
                }

        return {
            "lat": round(curr_lat, 5),
            "lon": round(curr_lon, 5),
            "location_name": location_name,
            "speed_kmh": base_speed,
            "vibration_g": vibration_g,
            "is_hitting_pothole": is_hitting_pothole,
            "precaution": proactive_precaution,
            "progress_pct": int((step_idx % 100))
        }
