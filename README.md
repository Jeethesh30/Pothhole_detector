# Bengaluru Road Hazard & Pothole AI Detector

A Streamlit-based web application for detecting potholes and road hazards using computer vision, live telemetry simulation, and Bengaluru infrastructure reporting tools.

## Features

- Live camera capture and automatic pothole detection
- YOLOv8 model loading with optional custom weights upload
- Route telemetry and simulated GPS-based hazard alerts
- Media inspection studio for uploaded road images
- Spatial analytics dashboard for Bengaluru ward data
- BBMP report generation in HTML and PDF formats

## Tech Stack

- Python 3.11
- Streamlit
- OpenCV
- Ultralytics YOLOv8
- Plotly
- Folium
- Pandas
- ReportLab

## Local Setup

1. Clone the repository.
2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

## Docker Run

```bash
docker build -t pothole-detector .
docker run -p 8501:8501 pothole-detector
```

Then open: http://localhost:8501

## Publishing / Deployment

### Option 1: GitHub + Render

1. Push the project to GitHub.
2. Create a new Render Web Service.
3. Connect the GitHub repo.
4. Use the existing Dockerfile for deployment.
5. Set the service to port 8501.

### Option 2: GitHub + Streamlit Community Cloud

1. Push the repo to GitHub.
2. Import the repo in Streamlit Cloud.
3. Choose the app entry as `app.py`.
4. Ensure requirements are in `requirements.txt`.

### Option 3: Docker Hub / container registry

```bash
docker build -t your-username/pothole-detector:latest .
docker push your-username/pothole-detector:latest
```

## Notes

- The default model weights are loaded from the local `models` directory.
- You can upload a custom `.pt` YOLOv8 model from the sidebar in the app.
- For production hosting, consider using a remote model store or preloading weights into the deployment image.

## License

This project is intended for demonstration and local deployment purposes. Add an appropriate license before public release if you plan to distribute it widely.
