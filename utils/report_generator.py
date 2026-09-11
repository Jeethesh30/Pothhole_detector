"""
BBMP Civic Grievance & Pothole Hazard Report Generator (HTML & PDF)
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_bbmp_html_report(report_data):
    """Generates clean, printable HTML civic complaint document."""
    date_str = report_data.get("timestamp", datetime.now().strftime("%d-%b-%Y %H:%M"))
    report_id = report_data.get("report_id", f"BBMP-GRV-{datetime.now().strftime('%Y%m%d%H%M')}")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>BBMP Road Defect Grievance Report - {report_id}</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: #222;
                margin: 40px;
                line-height: 1.6;
            }}
            .header {{
                border-bottom: 3px solid #1a365d;
                padding-bottom: 12px;
                margin-bottom: 24px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .org-title {{
                font-size: 20px;
                font-weight: bold;
                color: #1a365d;
                text-transform: uppercase;
                margin: 0;
            }}
            .sub-title {{
                font-size: 13px;
                color: #4a5568;
                margin-top: 4px;
            }}
            .badge-urgent {{
                background-color: #e53e3e;
                color: white;
                padding: 6px 14px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
                text-transform: uppercase;
            }}
            .section-title {{
                font-size: 15px;
                font-weight: bold;
                color: #2b6cb0;
                border-left: 4px solid #2b6cb0;
                padding-left: 10px;
                margin-top: 24px;
                margin-bottom: 12px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            th, td {{
                border: 1px solid #cbd5e0;
                padding: 10px 12px;
                text-align: left;
                font-size: 13px;
            }}
            th {{
                background-color: #f7fafc;
                color: #2d3748;
                font-weight: bold;
            }}
            .footer {{
                margin-top: 40px;
                border-top: 1px solid #e2e8f0;
                padding-top: 12px;
                font-size: 11px;
                color: #718096;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <div class="org-title">Bruhat Bengaluru Mahanagara Palike (BBMP)</div>
                <div class="sub-title">Road Infrastructure & Public Safety Hazard Notice</div>
            </div>
            <div class="badge-urgent">PRIORITY REPAIR NOTICE</div>
        </div>

        <div style="margin-bottom: 20px; font-size: 13px;">
            <strong>Grievance Reference ID:</strong> {report_id}<br>
            <strong>Date & Timestamp:</strong> {date_str}<br>
            <strong>Reporter Name:</strong> {report_data.get('reporter_name', 'Bengaluru Citizen Inspector')}<br>
            <strong>Assigned Authority:</strong> BBMP Road Infrastructure Division & Traffic Police
        </div>

        <div class="section-title">1. Hazard Location & Spatial Coordinates</div>
        <table>
            <tr><th>Location / Landmark</th><td>{report_data.get('location_name', 'Outer Ring Road, Bellandur')}</td></tr>
            <tr><th>BBMP Administrative Ward</th><td>{report_data.get('ward', 'Ward 150 (Bellandur)')}</td></tr>
            <tr><th>GPS Coordinates</th><td>Lat: {report_data.get('lat', '12.9366')}, Lon: {report_data.get('lon', '77.6963')}</td></tr>
        </table>

        <div class="section-title">2. AI Telemetry & YOLOv8 Computer Vision Inspection</div>
        <table>
            <tr><th>Hazard Severity Rating</th><td><strong>{report_data.get('severity', 'Severe')}</strong></td></tr>
            <tr><th>YOLOv8 AI Model Confidence</th><td>{report_data.get('confidence', '94%')}</td></tr>
            <tr><th>Estimated Defect Depth</th><td>{report_data.get('depth_cm', '12.5')} cm</td></tr>
            <tr><th>Estimated Surface Area</th><td>{report_data.get('area_m2', '0.85')} m²</td></tr>
            <tr><th>Accelerometer Impact Shock</th><td>{report_data.get('vibration_g', '3.4')} g-force</td></tr>
        </table>

        <div class="section-title">3. Recommended Municipal Action & Safety Precaution</div>
        <div style="background-color: #ebf8ff; border: 1px solid #bee3f8; padding: 14px; border-radius: 6px; font-size: 13px; color: #2b6cb0;">
            <strong>Immediate Directives:</strong><br>
            1. Deploy emergency road barrier/warning cone at location GPS coordinates within 12 hours.<br>
            2. Schedule cold-mix asphalt filling or asphalt milling repair by BBMP Ward Engineer team.<br>
            3. Issue precautionary traffic speed limit advisory (20 km/h) for approaching corridor vehicles.
        </div>

        <div class="footer">
            Automated Grievance Document generated by Bengaluru Road Hazard AI Detection System.<br>
            Official Copy for BBMP Grievance Cell (Sahaya 2.0 / Namma Bengaluru Portal).
        </div>
    </body>
    </html>
    """
    return html_content

def generate_bbmp_pdf_report(report_data):
    """Generates downloadable PDF report using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor('#4a5568'),
        spaceAfter=12
    )
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=14,
        spaceAfter=8
    )
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2d3748')
    )

    # Document Header
    story.append(Paragraph("BRUHAT BENGALURU MAHANAGARA PALIKE (BBMP)", title_style))
    story.append(Paragraph("ROAD INFRASTRUCTURE & PUBLIC SAFETY GRIEVANCE NOTICE", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a365d'), spaceAfter=14))

    # Reference Details
    date_str = report_data.get("timestamp", datetime.now().strftime("%d-%b-%Y %H:%M"))
    report_id = report_data.get("report_id", f"BBMP-GRV-{datetime.now().strftime('%Y%m%d%H%M')}")
    
    ref_data = [
        [Paragraph(f"<b>Grievance ID:</b> {report_id}", body_style), Paragraph(f"<b>Timestamp:</b> {date_str}", body_style)],
        [Paragraph(f"<b>Reporter:</b> {report_data.get('reporter_name', 'Citizen Inspector')}", body_style), Paragraph("<b>Priority:</b> URGENT ROAD REPAIR", body_style)]
    ]
    t_ref = Table(ref_data, colWidths=[270, 270])
    t_ref.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_ref)

    # Section 1: Location
    story.append(Paragraph("1. Hazard Location & Spatial Coordinates", section_style))
    loc_table_data = [
        [Paragraph("<b>Landmark / Street</b>", body_style), Paragraph(str(report_data.get('location_name', 'Outer Ring Road')), body_style)],
        [Paragraph("<b>BBMP Ward</b>", body_style), Paragraph(str(report_data.get('ward', 'Ward 150 (Bellandur)')), body_style)],
        [Paragraph("<b>GPS Coordinates</b>", body_style), Paragraph(f"Lat: {report_data.get('lat', '12.9366')}, Lon: {report_data.get('lon', '77.6963')}", body_style)]
    ]
    t_loc = Table(loc_table_data, colWidths=[160, 380])
    t_loc.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_loc)

    # Section 2: AI Telemetry
    story.append(Paragraph("2. AI Telemetry & Detection Metrics", section_style))
    ai_table_data = [
        [Paragraph("<b>Hazard Severity</b>", body_style), Paragraph(f"<b>{report_data.get('severity', 'Severe')}</b>", body_style)],
        [Paragraph("<b>AI Model Confidence</b>", body_style), Paragraph(str(report_data.get('confidence', '94%')), body_style)],
        [Paragraph("<b>Est. Depth & Area</b>", body_style), Paragraph(f"{report_data.get('depth_cm', '12.5')} cm depth | {report_data.get('area_m2', '0.85')} m² area", body_style)],
        [Paragraph("<b>Vibration Shock</b>", body_style), Paragraph(f"{report_data.get('vibration_g', '3.4')} g-force impact", body_style)]
    ]
    t_ai = Table(ai_table_data, colWidths=[160, 380])
    t_ai.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_ai)

    # Section 3: Directives
    story.append(Paragraph("3. Recommended BBMP Engineering Action", section_style))
    directives = Paragraph(
        "<b>Immediate Action Required:</b><br/>"
        "1. Deploy warning barricades at GPS coordinates immediately.<br/>"
        "2. Dispatch BBMP Ward asphalt repair team within 24 hours.<br/>"
        "3. Issue precautionary hazard alert to traffic navigation feeds.",
        body_style
    )
    t_dir = Table([[directives]], colWidths=[540])
    t_dir.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ebf8ff')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#bee3f8')),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_dir)

    # Build PDF document
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
