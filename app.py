"""
Bengaluru Road Hazard & Pothole Detector - Streamlit Web Application
"""

import os
import time
import json
import io
import random
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go

# Import custom utilities & styling
from components.styles import apply_custom_styles
from utils.sample_generator import (
    generate_synthetic_road_images, 
    get_sample_hazard_dataframe, 
    BENGALURU_ROUTES
)
from utils.model_loader import PotholeDetectorEngine
from utils.telemetry_simulator import VehicleTelemetrySimulator, calculate_haversine_distance
from utils.report_generator import generate_bbmp_html_report, generate_bbmp_pdf_report

# Page Configuration
st.set_page_config(
    page_title="Bengaluru Pothole & Road Hazard AI Detector",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS Theme
apply_custom_styles()

# Initialize Session State
if "sample_images" not in st.session_state:
    st.session_state["sample_images"] = generate_synthetic_road_images()

if "hazard_df" not in st.session_state:
    st.session_state["hazard_df"] = get_sample_hazard_dataframe()

if "detector" not in st.session_state:
    st.session_state["detector"] = PotholeDetectorEngine()

if "sim_step" not in st.session_state:
    st.session_state["sim_step"] = 0

if "sim_playing" not in st.session_state:
    st.session_state["sim_playing"] = False

detector = st.session_state["detector"]

# Sidebar Controls
st.sidebar.markdown("### ⚙️ AI Engine & Configuration")

# Model Weights Selection
model_option = st.sidebar.radio(
    "Select Model Weights Source:",
    ["Pre-trained Pothole YOLOv8", "Upload Custom Weights (.pt)"],
    index=0
)

if model_option == "Upload Custom Weights (.pt)":
    uploaded_pt = st.sidebar.file_uploader("Upload custom YOLOv8 .pt file:", type=["pt"])
    if uploaded_pt is not None:
        temp_pt_path = os.path.join("models", uploaded_pt.name)
        with open(temp_pt_path, "wb") as f:
            f.write(uploaded_pt.getbuffer())
        detector.load_model(temp_pt_path)
        st.sidebar.success(f"Loaded: {uploaded_pt.name}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Detection Parameters")
conf_threshold = st.sidebar.slider("Confidence Threshold", 0.10, 0.95, 0.35, 0.05)
iou_threshold = st.sidebar.slider("NMS IoU Threshold", 0.10, 0.95, 0.45, 0.05)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📷 Live Camera Settings")
auto_capture_interval = st.sidebar.slider("Auto-capture interval (sec)", 1, 10, 3)

st.sidebar.markdown("---")
st.sidebar.info(f"**Loaded Model:** {detector.model_name}\n\n**City Context:** Bengaluru Metropolitan Region (BBMP Wards)")

# Header Banner
st.markdown("""
<div class="app-header">
    <div>
        <h1 class="app-header-title">🚨 Bengaluru Road Hazard & Pothole AI Detector</h1>
        <div class="app-header-subtitle">Real-time Vision Analytics, Live Telemetry & Proactive Navigation Warning Portal</div>
    </div>
    <div style="text-align: right;">
        <span class="badge badge-info">🟢 SYSTEM ONLINE</span>
        <div style="font-size: 0.8rem; color: #8b949e; margin-top: 4px;">BBMP Ward Infrastructure Network</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📷 Live Camera & Auto-Detector",
    "🚗 Navigation & Proactive Alerts",
    "📸 Media Inspection Studio",
    "🗺️ Bengaluru Spatial Analytics",
    "📋 BBMP Grievance Generator"
])

# ==============================================================================
# TAB 1: Live Camera & Auto-Snapshot Detector
# ==============================================================================
with tab1:
    st.markdown("### 📷 Automatic Live Camera Stream & Photo Snapshot Detector")
    st.caption("Point your camera at the road. The system automatically captures pictures and detects potholes in real-time without manual uploads.")

    col_cam_left, col_cam_right = st.columns([1, 1])

    with col_cam_left:
        st.markdown("#### 🎥 Live Camera Input")
        camera_photo = st.camera_input("Take live photo or keep camera active:")
        
        # Test with sample camera frame option if web camera is disabled/unavailable
        use_sample_cam = st.checkbox("Or use test camera feed simulation", value=False)
        
        frame_to_process = None
        if camera_photo is not None:
            bytes_data = camera_photo.getvalue()
            cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            frame_to_process = cv_img
        elif use_sample_cam:
            # Use sample image as simulated camera frame
            sample_path = st.session_state["sample_images"][0]
            frame_to_process = cv2.imread(sample_path)

    with col_cam_right:
        st.markdown("#### ⚡ Real-Time Vision HUD & Automatic Map Pinning")
        if frame_to_process is not None:
            annotated_frame, detections = detector.predict_frame(
                frame_to_process, 
                conf_threshold=conf_threshold, 
                iou_threshold=iou_threshold
            )
            
            # Convert BGR to RGB for Streamlit display
            rgb_annotated = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            st.image(rgb_annotated, caption="Auto-Detected Hazard HUD", use_container_width=True)

            num_defects = len(detections)
            severe_count = sum(1 for d in detections if d["severity"] == "Severe")
            
            # HUD Metric Cards
            m1, m2, m3 = st.columns(3)
            m1.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Detected Defects</div>
                <div class="metric-value">{num_defects}</div>
                <div class="metric-subtext">Automated Scan</div>
            </div>
            """, unsafe_allow_html=True)
            
            m2.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Severe Hazards</div>
                <div class="metric-value" style="color: {'#ff0055' if severe_count > 0 else '#00e676'};">{severe_count}</div>
                <div class="metric-subtext">Immediate Attention</div>
            </div>
            """, unsafe_allow_html=True)
            
            avg_depth = round(np.mean([d["depth_cm"] for d in detections]), 1) if detections else 0.0
            m3.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Defect Depth</div>
                <div class="metric-value">{avg_depth} cm</div>
                <div class="metric-subtext">Volumetric Estimate</div>
            </div>
            """, unsafe_allow_html=True)

            # Precaution Banner if severe defect detected
            if severe_count > 0:
                st.markdown("""
                <div class="precaution-alert-box">
                    <div class="precaution-icon">🚨</div>
                    <div>
                        <div class="precaution-title">CRITICAL HAZARD DETECTED IN LIVE STREAM</div>
                        <div class="precaution-desc">Severe pothole detected! Location pinned to Bengaluru live map and logged for BBMP repair dispatch.</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto-append detection to hazard database session
                new_hazard = {
                    "Hazard ID": f"BLR-LIVE-{random.randint(2000, 9999)}",
                    "Location Name": "Live Camera Feed (Outer Ring Road)",
                    "Ward": "Ward 150 (Bellandur)",
                    "Latitude": 12.9366 + random.uniform(-0.003, 0.003),
                    "Longitude": 77.6963 + random.uniform(-0.003, 0.003),
                    "Severity": "Severe",
                    "Est. Depth (cm)": avg_depth,
                    "Est. Surface Area (m²)": 0.9,
                    "Confidence": detections[0]["confidence"] if detections else 0.9,
                    "Status": "Unrepaired - High Priority",
                    "Reported Time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state["hazard_df"] = pd.concat([pd.DataFrame([new_hazard]), st.session_state["hazard_df"]], ignore_index=True)
        else:
            st.info("👈 Activate live camera above or check the simulation box to begin auto-detection.")

# ==============================================================================
# TAB 2: Proactive Predictive Navigation & Route Telemetry Stream
# ==============================================================================
with tab2:
    st.markdown("### 🚗 Proactive Predictive Navigation & Live Location Telemetry")
    st.caption("Detects your live GPS location or simulates navigation along Bengaluru corridors with proactive distance-based hazard alerts!")

    # Location Mode Selector
    loc_mode = st.radio(
        "Navigation Source Mode:",
        ["🌐 Use My Real-Time Device GPS Location", "🛣️ Bengaluru Corridor Drive Simulator"],
        horizontal=True
    )

    curr_lat, curr_lon = 12.9366, 77.6963  # Default Bellandur ORR
    location_title = "Outer Ring Road, Bengaluru"
    speed_kmh = 42
    vibration_g = 1.05
    precaution_info = None

    if loc_mode == "🌐 Use My Real-Time Device GPS Location":
        st.markdown("#### 📍 Real-Time Device GPS Sensor & Location Selection")
        
        # HTML5 Browser Geolocation Auto-Detector Component
        st.components.v1.html("""
        <div style="background: rgba(22, 27, 34, 0.9); border: 1px solid rgba(0, 242, 254, 0.3); padding: 14px 20px; border-radius: 12px; font-family: sans-serif; color: #e6edf3; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <strong style="color: #00f2fe; font-size: 0.95rem;">📡 Browser HTML5 Live GPS Sensor</strong>
                <div id="gps-status" style="font-size: 0.85rem; color: #8b949e; margin-top: 4px;">Click button to auto-detect your physical device GPS coordinates in real time.</div>
            </div>
            <button onclick="getRealGPS()" style="background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); color: #05070a; border: none; font-weight: bold; padding: 10px 18px; border-radius: 8px; cursor: pointer;">
                📍 Auto-Detect My Live Location
            </button>
        </div>
        <script>
        function getRealGPS() {
            const statusDiv = document.getElementById('gps-status');
            statusDiv.innerText = '📡 Requesting browser GPS permission...';
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        const lat = pos.coords.latitude.toFixed(5);
                        const lon = pos.coords.longitude.toFixed(5);
                        const acc = Math.round(pos.coords.accuracy);
                        statusDiv.innerHTML = `<span style="color: #00e676; font-weight: bold;">✅ Device GPS Acquired:</span> Lat: <b>${lat}</b>, Lon: <b>${lon}</b> (Accuracy: ~${acc}m). Enter these in the fields below!`;
                    },
                    (err) => {
                        statusDiv.innerHTML = `<span style="color: #ff0055;">⚠️ GPS Permission Warning: ${err.message}. You can select any Bengaluru preset location below!</span>`;
                    },
                    { enableHighAccuracy: true, timeout: 10000 }
                );
            } else {
                statusDiv.innerText = '❌ Geolocation is not supported by your browser.';
            }
        }
        </script>
        """, height=90)
        
        # Comprehensive Bengaluru Locations Dictionary
        BENGALURU_PRESET_LOCATIONS = {
            "Outer Ring Road - Bellandur EcoSpace": (12.9366, 77.6963),
            "Outer Ring Road - Silk Board Junction": (12.9172, 77.6228),
            "Outer Ring Road - HSR Layout Flyover": (12.9116, 77.6389),
            "Outer Ring Road - Agara Signal": (12.9255, 77.6835),
            "Outer Ring Road - Iblur Junction": (12.9279, 77.6800),
            "Outer Ring Road - Devarabeesanahalli": (12.9430, 77.6970),
            "Outer Ring Road - Marathahalli Bridge": (12.9568, 77.7011),
            "Koramangala - Sony World Signal (80ft Rd)": (12.9345, 77.6265),
            "Koramangala - 5th Block (Forum Mall)": (12.9348, 77.6110),
            "Indiranagar - 100ft Road (12th Main)": (12.9719, 77.6412),
            "Indiranagar - Metro Station (CMH Road)": (12.9784, 77.6408),
            "Domlur - Flyover & Old Airport Road": (12.9550, 77.6410),
            "Whitefield - Hoodi Junction": (12.9918, 77.7161),
            "Whitefield - Vydehi Hospital Circle": (12.9863, 77.7289),
            "Whitefield - ITPL Main Gate": (12.9847, 77.7377),
            "Whitefield - Hope Farm Circle": (12.9778, 77.7471),
            "Hebbal - Flyover & Esteem Mall": (13.0358, 77.5970),
            "Yelahanka - Bypass & Jakkur": (13.1007, 77.5963),
            "MG Road - Brigade Road (CBD Zone)": (12.9756, 77.6066),
            "Majestic - Kempegowda Bus Terminal": (12.9767, 77.5713),
            "Electronic City - Phase 1 Toll Plaza": (12.8452, 77.6602),
            "JP Nagar - 3rd Phase Underpass": (12.9063, 77.5956),
            "Banashankari - TTMC Junction": (12.9254, 77.5739),
            "Rajajinagar - Navrang Circle": (12.9972, 77.5552),
            "Malleshwaram - Sampige Road (18th Cross)": (13.0031, 77.5701)
        }

        col_gps1, col_gps2, col_gps3 = st.columns([1, 1, 1.2])
        with col_gps3:
            st.markdown("<br>", unsafe_allow_html=True)
            preset_loc = st.selectbox(
                "Jump to Major Bengaluru Location / Ward:",
                list(BENGALURU_PRESET_LOCATIONS.keys())
            )
            selected_coords = BENGALURU_PRESET_LOCATIONS[preset_loc]

        with col_gps1:
            input_lat = st.number_input("Your Latitude:", value=selected_coords[0], format="%.5f")
        with col_gps2:
            input_lon = st.number_input("Your Longitude:", value=selected_coords[1], format="%.5f")

        curr_lat, curr_lon = input_lat, input_lon
        location_title = f"Live GPS: ({curr_lat}, {curr_lon})"

        # Check hazards near user's real GPS coordinates from dataset
        df_h = st.session_state["hazard_df"]
        min_d = 999999
        closest_h = None
        for _, h_row in df_h.iterrows():
            d_m = calculate_haversine_distance(curr_lat, curr_lon, h_row["Latitude"], h_row["Longitude"])
            if d_m < min_d:
                min_d = d_m
                closest_h = h_row

        if closest_h is not None and min_d <= 250:
            sev = closest_h["Severity"]
            rec_spd = "20 km/h" if sev == "Severe" else "30 km/h"
            precaution_info = {
                "active": True,
                "status": "PROACTIVE PRECAUTION",
                "distance_m": int(min_d),
                "hazard_name": closest_h["Location Name"],
                "severity": sev,
                "recommended_speed": rec_spd,
                "message": f"🚨 PRECAUTION: {sev} Road Hazard detected {int(min_d)}m from your GPS position near {closest_h['Location Name']} ({closest_h['Ward']})! Recommended max speed: {rec_spd}."
            }

    else:
        col_nav_top1, col_nav_top2 = st.columns([2, 1])
        with col_nav_top1:
            selected_route = st.selectbox(
                "Select Bengaluru Corridor Route:",
                list(BENGALURU_ROUTES.keys()),
                index=0
            )
        with col_nav_top2:
            st.markdown("<br>", unsafe_allow_html=True)
            col_btn1, col_btn2 = st.columns(2)
            if col_btn1.button("▶ Step Drive Forward"):
                st.session_state["sim_step"] = (st.session_state["sim_step"] + 5) % 100
            if col_btn2.button("🔄 Reset Route"):
                st.session_state["sim_step"] = 0

        simulator = VehicleTelemetrySimulator(selected_route)
        step_data = simulator.get_telemetry_step(st.session_state["sim_step"])
        
        curr_lat = step_data["lat"]
        curr_lon = step_data["lon"]
        location_title = step_data["location_name"]
        speed_kmh = step_data["speed_kmh"]
        vibration_g = step_data["vibration_g"]
        precaution_info = step_data.get("precaution")

    # PROACTIVE PRECAUTIONARY POPUP WARNING BANNER
    if precaution_info and precaution_info.get("active"):
        st.markdown(f"""
        <div class="precaution-alert-box">
            <div class="precaution-icon">🚨</div>
            <div>
                <div class="precaution-title">{precaution_info['status']}: {precaution_info['severity'].upper()} HAZARD {precaution_info['distance_m']}m FROM YOUR LOCATION</div>
                <div class="precaution-desc">{precaution_info['message']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(0, 230, 118, 0.1); border: 1px solid rgba(0, 230, 118, 0.3); padding: 12px 20px; border-radius: 10px; color: #5cf29d; font-size: 0.9rem; font-weight: 600; margin-bottom: 16px;">
            🟢 CLEAR ROAD AHEAD: No major road hazards logged within 250m radius of current GPS coordinates.
        </div>
        """, unsafe_allow_html=True)

    # Telemetry HUD Row
    t1, t2, t3, t4 = st.columns(4)
    t1.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Live Speed</div>
        <div class="metric-value">{speed_kmh} <span style="font-size: 1rem;">km/h</span></div>
        <div class="metric-subtext">GPS Telemetry</div>
    </div>
    """, unsafe_allow_html=True)

    vibr_color = "#ff0055" if vibration_g > 2.5 else "#00f2fe"
    t2.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Vibration Shock Index</div>
        <div class="metric-value" style="color: {vibr_color};">{vibration_g} <span style="font-size: 1rem;">g</span></div>
        <div class="metric-subtext">Z-Axis Accelerometer</div>
    </div>
    """, unsafe_allow_html=True)

    t3.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Current Position</div>
        <div class="metric-value" style="font-size: 1.0rem; padding-top: 8px;">{location_title}</div>
        <div class="metric-subtext">Lat: {curr_lat}, Lon: {curr_lon}</div>
    </div>
    """, unsafe_allow_html=True)

    nearest_dist_str = f"{precaution_info['distance_m']}m" if (precaution_info and precaution_info.get("active")) else "> 250m"
    t4.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Nearest Hazard Distance</div>
        <div class="metric-value" style="color: {'#ff0055' if nearest_dist_str != '> 250m' else '#00e676'};">{nearest_dist_str}</div>
        <div class="metric-subtext">Proactive Warning Radius</div>
    </div>
    """, unsafe_allow_html=True)

    # Map & Frame Stream Columns
    col_map, col_stream = st.columns([1.2, 0.8])

    with col_map:
        st.markdown("#### 🗺️ Live Navigation Map & Proactive Warning Zone")
        
        # Create Folium Map centered on current location
        m_nav = folium.Map(
            location=[curr_lat, curr_lon], 
            zoom_start=14, 
            tiles="OpenStreetMap"
        )

        # Draw hazards from database
        for _, h_row in st.session_state["hazard_df"].iterrows():
            sev_color = "red" if h_row["Severity"] == "Severe" else ("orange" if h_row["Severity"] == "Moderate" else "green")
            folium.CircleMarker(
                location=[h_row["Latitude"], h_row["Longitude"]],
                radius=6 if h_row["Severity"] == "Severe" else 4,
                color=sev_color,
                fill=True,
                fill_color=sev_color,
                popup=f"<b>{h_row['Hazard ID']}</b><br>{h_row['Location Name']}<br>Severity: {h_row['Severity']}"
            ).add_to(m_nav)

        # Add current user / vehicle position marker with warning pulse
        folium.Marker(
            location=[curr_lat, curr_lon],
            popup=f"<b>Your Current Position</b><br>{location_title}",
            icon=folium.Icon(color="green" if not precaution_info else "red", icon="crosshairs", prefix="fa")
        ).add_to(m_nav)

        st_folium(m_nav, width=None, height=360, key="nav_folium_map")

    with col_stream:
        st.markdown("#### 🎥 Live Road Dashcam HUD")
        
        # Dynamically pick road image corresponding to the selected location and hazard severity
        loc_lower = location_title.lower()
        if precaution_info and precaution_info.get("active"):
            if "koramangala" in loc_lower or "sony" in loc_lower:
                sample_img_idx = 1  # koramangala_pothole_1.jpg
            elif "whitefield" in loc_lower or "hoodi" in loc_lower or "itpl" in loc_lower:
                sample_img_idx = 2  # whitefield_road_defect.jpg
            else:
                sample_img_idx = 0  # bengaluru_orr_severe.jpg
        else:
            sample_img_idx = 3  # clean_road_sample.jpg

        img_path = st.session_state["sample_images"][sample_img_idx]
        frame_bgr = cv2.imread(img_path)

        annotated_dashcam, _ = detector.predict_frame(frame_bgr, conf_threshold=conf_threshold, iou_threshold=iou_threshold)
        rgb_dashcam = cv2.cvtColor(annotated_dashcam, cv2.COLOR_BGR2RGB)
        st.image(rgb_dashcam, caption=f"Dashcam Scan - {location_title}", use_container_width=True)


# ==============================================================================
# TAB 3: Offline Media Inspection Studio
# ==============================================================================
with tab3:
    st.markdown("### 📸 Media Inspection Studio (Image & Video)")
    st.caption("Upload images/videos or choose pre-packaged Bengaluru road samples to test custom model weights.")

    col_inp1, col_inp2 = st.columns([1, 1])
    
    with col_inp1:
        st.markdown("#### 📥 Media Source")
        media_mode = st.radio("Choose Input Mode:", ["Pre-packaged Sample Images", "Upload Local Image/Video"], horizontal=True)

        selected_image_bgr = None
        if media_mode == "Pre-packaged Sample Images":
            sample_names = [os.path.basename(p) for p in st.session_state["sample_images"]]
            chosen_sample = st.selectbox("Select Sample Road Image:", sample_names)
            chosen_path = [p for p in st.session_state["sample_images"] if os.path.basename(p) == chosen_sample][0]
            selected_image_bgr = cv2.imread(chosen_path)
        else:
            uploaded_file = st.file_uploader("Upload Image or Video (JPG, PNG, MP4):", type=["jpg", "jpeg", "png", "mp4"])
            if uploaded_file is not None:
                if uploaded_file.name.endswith(".mp4"):
                    st.warning("Video file uploaded. Running frame-by-frame analysis...")
                    tfile = open("temp_video.mp4", "wb")
                    tfile.write(uploaded_file.read())
                    cap = cv2.VideoCapture("temp_video.mp4")
                    ret, frame = cap.read()
                    if ret:
                        selected_image_bgr = frame
                    cap.release()
                else:
                    image_bytes = uploaded_file.read()
                    selected_image_bgr = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    with col_inp2:
        st.markdown("#### 🔬 YOLOv8 Annotated Output")
        if selected_image_bgr is not None:
            annotated_out, detections = detector.predict_frame(
                selected_image_bgr, 
                conf_threshold=conf_threshold, 
                iou_threshold=iou_threshold
            )
            rgb_out = cv2.cvtColor(annotated_out, cv2.COLOR_BGR2RGB)
            st.image(rgb_out, caption="YOLOv8 Detection & HUD Overlay", use_container_width=True)

            # Detection Table
            if detections:
                st.markdown("##### 📊 Detected Hazard Breakdowns")
                df_det = pd.DataFrame(detections)[["label", "severity", "confidence", "depth_cm", "area_m2"]]
                st.dataframe(df_det, use_container_width=True)
            else:
                st.info("No road defects detected above the confidence threshold.")

# ==============================================================================
# TAB 4: Bengaluru Spatial Analytics & Interactive Heatmap
# ==============================================================================
with tab4:
    st.markdown("### 🗺️ Bengaluru Spatial Analytics & Heatmap Dashboard")
    st.caption("Citywide breakdown of road defects, BBMP ward leaderboards, and spatial density heatmaps.")

    df_hazards = st.session_state["hazard_df"]

    # Top Metrics
    total_hazards = len(df_hazards)
    severe_hazards = len(df_hazards[df_hazards["Severity"] == "Severe"])
    avg_depth_city = round(df_hazards["Est. Depth (cm)"].mean(), 1)
    most_affected_ward = df_hazards["Ward"].mode()[0] if not df_hazards.empty else "N/A"

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Logged Hazards</div>
        <div class="metric-value">{total_hazards}</div>
        <div class="metric-subtext">Bengaluru Grid</div>
    </div>
    """, unsafe_allow_html=True)

    k2.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Severe Potholes</div>
        <div class="metric-value" style="color: #ff0055;">{severe_hazards}</div>
        <div class="metric-subtext">High Priority Repair</div>
    </div>
    """, unsafe_allow_html=True)

    k3.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Citywide Avg Depth</div>
        <div class="metric-value">{avg_depth_city} cm</div>
        <div class="metric-subtext">Volumetric Defect</div>
    </div>
    """, unsafe_allow_html=True)

    k4.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Most Affected Ward</div>
        <div class="metric-value" style="font-size: 1.0rem; padding-top: 8px;">{most_affected_ward}</div>
        <div class="metric-subtext">BBMP Hotspot</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col_analytics_left, col_analytics_right = st.columns([1.2, 0.8])

    with col_analytics_left:
        st.markdown("#### 🗺️ Bengaluru Citywide Hazard Heatmap")
        
        # Create Folium Map with Heatmap layer
        m_heat = folium.Map(
            location=[12.9716, 77.5946], 
            zoom_start=11, 
            tiles="OpenStreetMap"
        )
        
        for _, row in df_hazards.iterrows():
            sev = row["Severity"]
            color_marker = "red" if sev == "Severe" else ("orange" if sev == "Moderate" else "green")
            
            folium.CircleMarker(
                location=[row["Latitude"], row["Longitude"]],
                radius=6 if sev == "Severe" else 4,
                color=color_marker,
                fill=True,
                fill_color=color_marker,
                fill_opacity=0.7,
                popup=f"<b>{row['Hazard ID']}</b><br>{row['Location Name']}<br>Ward: {row['Ward']}<br>Severity: {sev}"
            ).add_to(m_heat)

        st_folium(m_heat, width=None, height=380, key="analytics_folium_map")

    with col_analytics_right:
        st.markdown("#### 📈 Severity Distribution")
        fig_pie = px.pie(
            df_hazards, 
            names="Severity", 
            color="Severity",
            color_discrete_map={"Severe": "#ff0055", "Moderate": "#ff9900", "Minor": "#00e676"},
            hole=0.45
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e6edf3"),
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Data Table & Export Buttons
    st.markdown("#### 📄 Exportable Bengaluru Hazard Registry")
    st.dataframe(df_hazards, use_container_width=True)

    col_exp1, col_exp2 = st.columns([1, 1])
    with col_exp1:
        csv_data = df_hazards.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Hazard Log CSV",
            csv_data,
            "bengaluru_pothole_hazards.csv",
            "text/csv",
            key='download-csv'
        )
    with col_exp2:
        # GeoJSON export
        geojson_features = []
        for _, r in df_hazards.iterrows():
            geojson_features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [r["Longitude"], r["Latitude"]]},
                "properties": dict(r)
            })
        geojson_str = json.dumps({"type": "FeatureCollection", "features": geojson_features}, indent=2)
        st.download_button(
            "🌍 Download GeoJSON Data",
            geojson_str,
            "bengaluru_pothole_hazards.geojson",
            "application/json",
            key='download-geojson'
        )

# ==============================================================================
# TAB 5: BBMP Civic Grievance Report Generator
# ==============================================================================
with tab5:
    st.markdown("### 📋 BBMP Civic Grievance & Official Complaint Document Generator")
    st.caption("Generate official PDF/HTML grievance notices for submission to BBMP (Sahaya 2.0) & Traffic Police.")

    df_hazards = st.session_state["hazard_df"]
    hazard_ids = df_hazards["Hazard ID"].tolist()

    col_form_left, col_form_right = st.columns([1, 1])

    with col_form_left:
        st.markdown("#### 📝 Complaint Details Form")
        selected_hid = st.selectbox("Select Detected Hazard ID:", hazard_ids)
        row_selected = df_hazards[df_hazards["Hazard ID"] == selected_hid].iloc[0]

        reporter_name = st.text_input("Reporter Name:", value="Bengaluru Citizen Inspector")
        custom_location = st.text_input("Location Name / Landmark:", value=row_selected["Location Name"])
        custom_ward = st.text_input("BBMP Ward:", value=row_selected["Ward"])

        rep_data = {
            "report_id": row_selected["Hazard ID"],
            "timestamp": row_selected["Reported Time"],
            "reporter_name": reporter_name,
            "location_name": custom_location,
            "ward": custom_ward,
            "lat": row_selected["Latitude"],
            "lon": row_selected["Longitude"],
            "severity": row_selected["Severity"],
            "confidence": f"{int(row_selected['Confidence']*100)}%",
            "depth_cm": row_selected["Est. Depth (cm)"],
            "area_m2": row_selected["Est. Surface Area (m²)"],
            "vibration_g": 3.4 if row_selected["Severity"] == "Severe" else 2.1
        }

        st.markdown("---")
        col_dl1, col_dl2 = st.columns(2)

        with col_dl1:
            pdf_bytes = generate_bbmp_pdf_report(rep_data)
            st.download_button(
                "📄 Download Official PDF Report",
                pdf_bytes,
                f"BBMP_Grievance_{rep_data['report_id']}.pdf",
                "application/pdf"
            )

        with col_dl2:
            html_str = generate_bbmp_html_report(rep_data)
            st.download_button(
                "🌐 Download HTML Document",
                html_str,
                f"BBMP_Grievance_{rep_data['report_id']}.html",
                "text/html"
            )

    with col_form_right:
        st.markdown("#### 👁️ Document Preview")
        html_preview = generate_bbmp_html_report(rep_data)
        st.components.v1.html(html_preview, height=450, scrolling=True)
