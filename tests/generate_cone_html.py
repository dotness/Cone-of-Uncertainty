"""
TEST SCRIPT: generate_cone_html.py
===================================
NOTE: This script is intended purely for User Acceptance Testing (UAT) purposes.
It dynamically parses local SQLite test databases to generate a visual HTML report
of the Cone of Uncertainty (including reversed cones) used in the UAT process.
It should not be used as part of the core production framework to generate
real-world cones without adaptation.
"""

import sqlite3
import json

def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_data():
    data = {}

    # LTV Database
    try:
        conn = get_db_connection('ltv_database.db')

        # Vision
        vision = conn.execute("SELECT * FROM ltv_vision ORDER BY id DESC LIMIT 1").fetchone()
        data['vision'] = dict(vision) if vision else None

        # Paths
        paths = conn.execute("SELECT * FROM cone_paths").fetchall()
        data['paths'] = [dict(p) for p in paths]

        # Node Points
        nodes = conn.execute("SELECT * FROM node_points").fetchall()
        data['nodes'] = [dict(n) for n in nodes]

        # False Cones
        false_cones = conn.execute("SELECT * FROM false_cones").fetchall()
        data['false_cones'] = [dict(fc) for fc in false_cones]

        conn.close()
    except Exception as e:
        print(f"Error reading ltv_database.db: {e}")

    # Cynefin Database
    try:
        conn = get_db_connection('skills/cynefin-domain-assessor/scripts/cynefin.db')
        assessments = conn.execute("SELECT * FROM assessments").fetchall()
        data['cynefin'] = [dict(a) for a in assessments]
        conn.close()
    except Exception as e:
        print(f"Error reading cynefin.db: {e}")

    # OODA Database
    try:
        conn = get_db_connection('skills/ooda-loop-navigator/scripts/ooda.db')
        loops = conn.execute("SELECT * FROM ooda_loops").fetchall()
        data['ooda'] = [dict(l) for l in loops]
        conn.close()
    except Exception as e:
        print(f"Error reading ooda.db: {e}")

    return data

def generate_html(data):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Antigravity AI - LTV Cone of Uncertainty</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f4f7f6;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 800px;
                margin: auto;
                padding: 20px;
            }
            h1, h2, h3 {
                color: #2c3e50;
            }
            .card {
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                padding: 20px;
                margin-bottom: 20px;
            }
            .vision-block {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            @media (min-width: 600px) {
                .vision-block {
                    flex-direction: row;
                }
                .vision-item {
                    flex: 1;
                }
            }
            .vision-item {
                background: #eef2f3;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #3498db;
            }
            .badge {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: bold;
                text-transform: uppercase;
            }
            .status-hypothetical { background: #f39c12; color: #fff; }
            .status-aligned { background: #2ecc71; color: #fff; }
            .status-eliminated { background: #e74c3c; color: #fff; }

            ul { list-style-type: none; padding: 0; }
            li {
                background: #fff;
                margin-bottom: 10px;
                padding: 15px;
                border-left: 4px solid #bdc3c7;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }

            .path-item.aligned { border-left-color: #2ecc71; }
            .path-item.eliminated { border-left-color: #e74c3c; }
            .path-item.hypothetical { border-left-color: #f39c12; }

            .cone-visual {
                background: #fff;
                padding: 30px;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                overflow-x: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="text-align: center;">Long Term Vision (LTV) Cone</h1>
    """

    # 1. Vision section
    vision = data.get('vision')
    if vision:
        html += f"""
            <div class="card">
                <h2>Vision Map</h2>
                <div class="vision-block">
                    <div class="vision-item">
                        <h3>AS-IS (Current State)</h3>
                        <p>{vision.get('as_is', 'N/A')}</p>
                    </div>
                    <div class="vision-item">
                        <h3>TO-BE (Future State)</h3>
                        <p>{vision.get('to_be', 'N/A')}</p>
                    </div>
                </div>
            </div>
        """

    # SVG Visual representation
    paths = data.get('paths', [])
    nodes = data.get('nodes', [])

    html += """
            <div class="cone-visual">
                <h2>Visual representation</h2>
                <svg width="100%" height="300" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
                    <!-- Cone Background -->
                    <path d="M 50 150 L 550 20 L 550 280 Z" fill="#eef2f3" stroke="#bdc3c7" stroke-width="2"/>

                    <!-- AS IS point -->
                    <circle cx="50" cy="150" r="8" fill="#34495e"/>
                    <text x="50" y="175" font-family="sans-serif" font-size="12" text-anchor="middle" font-weight="bold">AS-IS</text>

                    <!-- TO BE point -->
                    <circle cx="550" cy="150" r="10" fill="#2ecc71"/>
                    <text x="550" y="175" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="bold" fill="#2ecc71">TO-BE</text>
    """

    # Dynamically draw paths
    # We will spread them out. Aligned goes straight to TO-BE.
    # Hypothetical and eliminated paths angle up or down.

    y_offsets = [-80, 80, -40, 40, -100, 100]
    path_idx = 0

    for p in paths:
        status = p.get('status', 'hypothetical').lower()
        if status == 'aligned':
            html += f'<!-- Aligned Path (Center) -->\n'
            html += f'<line x1="50" y1="150" x2="550" y2="150" stroke="#2ecc71" stroke-width="3" stroke-dasharray="5,5" />\n'
            html += f'<text x="300" y="145" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#2ecc71">{p.get("name")}</text>\n'
        else:
            color = "#e74c3c" if status == "eliminated" else "#f39c12"
            y_end = 150 + y_offsets[path_idx % len(y_offsets)]
            dash = "" if status == "eliminated" else 'stroke-dasharray="3,3"'
            html += f'<line x1="50" y1="150" x2="480" y2="{y_end}" stroke="{color}" stroke-width="2" {dash} />\n'
            html += f'<text x="300" y="{150 + (y_end - 150)/2 - 5}" font-family="sans-serif" font-size="10" text-anchor="middle" fill="{color}">{p.get("name")}</text>\n'
            path_idx += 1

    # Dynamically draw nodes on the aligned path
    if nodes:
        spacing = 500 / (len(nodes) + 1)
        for i, n in enumerate(nodes):
            cx = 50 + (i + 1) * spacing
            html += f'<!-- Node Point {i+1} -->\n'
            html += f'<circle cx="{cx}" cy="150" r="6" fill="#8e44ad"/>\n'
            html += f'<text x="{cx}" y="135" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#8e44ad">{n.get("name")}</text>\n'

            # Draw reversed cone visually originating from node
            html += f'<path d="M {cx} 150 L {cx-40} 120 L {cx-40} 180 Z" fill="rgba(142, 68, 173, 0.1)" stroke="#8e44ad" stroke-width="1" stroke-dasharray="2,2"/>\n'

    html += """
                </svg>
                <p style="font-size: 0.8em; color: #7f8c8d; margin-top: 10px;">Diagram: Representation of the LTV Cone from AS-IS to TO-BE, showing aligned (green), hypothetical (orange), and eliminated (red) paths with backward-planned nodes and their associated reversed cones (purple triangles).</p>
            </div>
    """

    # 2. Cynefin Domain
    cynefin = data.get('cynefin', [])
    if cynefin:
        html += f"""
            <div class="card">
                <h2>Cynefin Domain Assessment</h2>
                <ul>
        """
        for c in cynefin:
            html += f"<li><strong>{c.get('name', '')}</strong>: <span class='badge' style='background:#9b59b6;color:#fff;'>{c.get('domain', '')}</span><br><small>{c.get('reason', '')}</small></li>"
        html += """
                </ul>
            </div>
        """

    # 3. Paths
    paths = data.get('paths', [])
    if paths:
        html += """
            <div class="card">
                <h2>Explored Paths</h2>
                <ul>
        """
        for p in paths:
            status = p.get('status', 'hypothetical').lower()
            html += f"""
                <li class="path-item {status}">
                    <strong>{p.get('name', 'N/A')}</strong>
                    <span class="badge status-{status}">{status}</span>
                    <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #555;">{p.get('description', '')}</p>
                </li>
            """
        html += """
                </ul>
            </div>
        """

    # 4. False Cones
    false_cones = data.get('false_cones', [])
    if false_cones:
        html += """
            <div class="card">
                <h2>Detected False Cones</h2>
                <ul>
        """
        for fc in false_cones:
            html += f"""
                <li style="border-left-color: #e74c3c;">
                    <strong>{fc.get('name', 'N/A')}</strong>
                    <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #555;"><em>Reason:</em> {fc.get('reason', '')}</p>
                </li>
            """
        html += """
                </ul>
            </div>
        """

    # 5. Node Points (Reversed Cone)
    nodes = data.get('nodes', [])
    if nodes:
        html += """
            <div class="card">
                <h2>Reversed Cone: Node Points</h2>
                <p><small>Milestones planned backward from TO-BE to AS-IS.</small></p>
                <ul>
        """
        for n in nodes:
            html += f"""
                <li style="border-left-color: #8e44ad;">
                    <strong>{n.get('name', 'N/A')}</strong> <small style="color:#7f8c8d;">({n.get('timestamp', '')})</small>
                    <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #555;">{n.get('description', '')}</p>
                </li>
            """
        html += """
                </ul>
            </div>
        """

    # 6. OODA Loops
    ooda = data.get('ooda', [])
    if ooda:
        html += """
            <div class="card">
                <h2>OODA Loops Navigation</h2>
                <ul>
        """
        for o in ooda:
            anomaly_badge = '<span class="badge" style="background:#e74c3c;color:#fff;">Anomaly Detected</span>' if o.get('anomaly_detected') else ''
            html += f"""
                <li style="border-left-color: #34495e;">
                    <strong>Target Node:</strong> {o.get('target_node', 'N/A')} {anomaly_badge}
                    <div style="margin-top: 10px; font-size: 0.9em;">
                        <strong>Observe:</strong> {o.get('observation', 'N/A')}<br>
                        <strong>Orient:</strong> {o.get('orientation_analysis', 'N/A')}<br>
                        <strong>Decide:</strong> {o.get('decision_hypothesis', 'N/A')}<br>
                        <strong>Act:</strong> {o.get('action_outcome', 'N/A')}<br>
                    </div>
                    <div style="margin-top: 10px; text-align: right;">
                        <span class="badge" style="background:#7f8c8d;color:#fff;">Status: {o.get('status', 'N/A')}</span>
                    </div>
                </li>
            """
        html += """
                </ul>
            </div>
        """

    html += """
        </div>
    </body>
    </html>
    """

    import os
    os.makedirs('tests/example_results', exist_ok=True)
    out_path = 'tests/example_results/cone_representation.html'

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Successfully generated {out_path}")

if __name__ == "__main__":
    db_data = fetch_data()
    generate_html(db_data)
