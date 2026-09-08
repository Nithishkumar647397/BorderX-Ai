import re

def update_file():
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update fonts
    html = html.replace('<head>', '<head>\n    <link rel="preconnect" href="https://fonts.googleapis.com">\n    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">')

    # 2. CSS variables
    old_vars = """        :root {
            --bg-base: #0a0a0a;
            --bg-panel: #161616;
            --bg-header: #1e1e1e;
            --bg-hover: #2a2a2a;
            --border: #333333;
            --border-light: #444444;
            --text-main: #e0e0e0;
            --text-muted: #888888;
            --text-dark: #111111;
            
            --risk-high: #d32f2f;
            --risk-attention: #f57c00;
            --risk-normal: #388e3c;
            --risk-unknown: #757575;
            
            --spacing: 8px;
            --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            --font-mono: 'Consolas', 'Courier New', monospace;
        }"""
    new_vars = """        :root {
            --bg-base: #0a0a0a;
            --bg-panel: #161616;
            --bg-header: #1e1e1e;
            --bg-hover: #2a2a2a;
            --border: #333333;
            --border-light: #444444;
            --text-main: #f4f4f5;
            --text-muted: #a1a1aa;
            --text-dark: #111111;
            
            --risk-high: #ef4444;
            --risk-attention: #f59e0b;
            --risk-normal: #22c55e;
            --risk-unknown: #71717a;
            
            --spacing: 16px;
            --font-family: 'Inter', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', 'Consolas', monospace;
        }"""
    html = html.replace(old_vars, new_vars)

    html = html.replace('font-size: 13px;', 'font-size: 14px;')

    # 3. Badges
    old_badges = """        .badge {
            padding: 2px 6px;
            border-radius: 2px;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-high { background: var(--risk-high); color: var(--text-dark); }
        .badge-attention { background: var(--risk-attention); color: var(--text-dark); }
        .badge-normal { background: var(--risk-normal); color: var(--text-dark); }"""
    new_badges = """        .badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            text-align: center;
        }
        .badge-high { background: var(--risk-high); color: #ffffff; text-shadow: 0 1px 2px rgba(0,0,0,0.4); }
        .badge-attention { background: var(--risk-attention); color: #000000; }
        .badge-normal { background: var(--risk-normal); color: #000000; }"""
    html = html.replace(old_badges, new_badges)

    # 4. Panel Header
    old_panel_header = """        .panel-header {
            padding: 6px 12px;
            background-color: var(--bg-header);
            border-bottom: 1px solid var(--border);
            font-weight: 600;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }"""
    new_panel_header = """        .panel-header {
            padding: 12px 16px;
            background-color: var(--bg-header);
            border-bottom: 1px solid var(--border);
            font-weight: 700;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }"""
    html = html.replace(old_panel_header, new_panel_header)

    # 5. Tables and lists
    old_tables = """        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }

        th, td {
            padding: 6px 10px;
            text-align: left;
            border-bottom: 1px solid var(--border);
            white-space: nowrap;
        }

        th {
            color: var(--text-muted);
            font-weight: 600;
            position: sticky;
            top: 0;
            background-color: var(--bg-panel);
            z-index: 5;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }"""
    new_tables = """        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }

        th, td {
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid var(--border);
            white-space: nowrap;
        }

        th {
            color: var(--text-muted);
            font-weight: 600;
            position: sticky;
            top: 0;
            background-color: var(--bg-panel);
            z-index: 5;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .text-right { text-align: right; }"""
    html = html.replace(old_tables, new_tables)

    old_list_item = """        .list-item {
            padding: 10px;
            border-bottom: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            gap: 6px;
        }"""
    new_list_item = """        .list-item {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            gap: 8px;
        }"""
    html = html.replace(old_list_item, new_list_item)

    # 6. Camera Feed
    old_camera_feed = """        .camera-feed {
            position: relative;
            background-color: #050505;
            border: 1px solid var(--border-light);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }"""
    new_camera_feed = """        .camera-feed {
            position: relative;
            background-color: #111;
            border: 1px solid var(--border-light);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: inset 0 0 60px rgba(0,0,0,0.9);
            filter: grayscale(15%) contrast(105%);
        }"""
    html = html.replace(old_camera_feed, new_camera_feed)

    old_camera_overlay = """        .camera-overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            padding: 8px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            z-index: 2;
            pointer-events: none;
            font-family: var(--font-mono);
            font-size: 11px;
            color: rgba(255, 255, 255, 0.85);
            text-shadow: 1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000;
        }"""
    new_camera_overlay = """        .camera-overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            padding: 12px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            z-index: 2;
            pointer-events: none;
            font-family: var(--font-mono);
            font-size: 12px;
            color: rgba(255, 255, 255, 0.95);
            text-shadow: 1px 1px 3px rgba(0,0,0,1);
        }
        .rec-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background-color: #ef4444;
            border-radius: 50%;
            margin-right: 6px;
            box-shadow: 0 0 4px #ef4444;
            animation: blink 2s infinite;
        }"""
    html = html.replace(old_camera_overlay, new_camera_overlay)

    # 7. Summary Charts
    old_summary_stats = """        .summary-stats {
            display: flex;
            flex-direction: column;
            gap: 16px;
            height: 100%;
            justify-content: center;
        }
        .stat-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .stat-label {
            font-size: 11px;
            text-transform: uppercase;
            width: 80px;
            color: var(--text-muted);
        }
        .stat-value {
            font-size: 18px;
            font-weight: 700;
            font-family: var(--font-mono);
            width: 40px;
            text-align: right;
        }
        .stat-bar {
            flex: 1;
            height: 4px;
            margin: 0 16px;
            background: var(--border);
        }
        .stat-bar-inner {
            height: 100%;
        }"""
    new_summary_stats = """        .summary-stats {
            display: flex;
            flex-direction: column;
            gap: 20px;
            height: 100%;
            justify-content: center;
        }
        .stat-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .stat-label {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            width: 80px;
            color: var(--text-muted);
        }
        .stat-value {
            font-size: 18px;
            font-weight: 700;
            font-family: var(--font-mono);
            width: 50px;
            text-align: right;
        }
        .stat-bar {
            flex: 1;
            height: 8px;
            margin: 0 16px;
            background: #222;
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid var(--border);
        }
        .stat-bar-inner {
            height: 100%;
            border-radius: 3px;
        }"""
    html = html.replace(old_summary_stats, new_summary_stats)

    # 8. Glance Strip CSS
    glance_css = """
        /* Glance Strip */
        #glance-strip {
            display: flex;
            align-items: center;
            background-color: var(--bg-panel);
            border-bottom: 1px solid var(--border);
            padding: 16px 24px;
            gap: 48px;
        }
        .glance-item {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .glance-label {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        .glance-value {
            font-size: 24px;
            font-weight: 700;
        }
        .glance-divider {
            width: 1px;
            height: 32px;
            background-color: var(--border);
        }
"""
    html = html.replace('        /* Scrollbar */', glance_css + '        /* Scrollbar */')

    # 9. Glance Strip HTML
    glance_html = """        </header>

        <!-- At A Glance Strip -->
        <div id="glance-strip">
            <div class="glance-item">
                <span class="glance-label">ACTIVE HIGH-RISK</span>
                <span class="glance-value text-high mono" id="glance-high-risk">0</span>
            </div>
            <div class="glance-divider"></div>
            <div class="glance-item">
                <span class="glance-label">CAMERAS ONLINE</span>
                <span class="glance-value mono">6/6</span>
            </div>
            <div class="glance-divider"></div>
            <div class="glance-item">
                <span class="glance-label">SYNC QUEUE</span>
                <span class="glance-value mono" id="glance-sync">0</span>
            </div>
            <div class="glance-divider"></div>
            <div class="glance-item">
                <span class="glance-label">NETWORK</span>
                <span class="glance-value text-normal" id="glance-network">ONLINE</span>
            </div>
        </div>

        <!-- Dashboard Grid -->"""
    html = html.replace('        </header>\n\n        <!-- Dashboard Grid -->', glance_html)

    # 10. Camera JS rendering
    old_camera_js = """                            <div class="camera-top-bar">
                                <span>${cam.id} - ${cam.name}</span>
                                <span class="text-high" style="font-size: 9px; animation: blink 2s infinite;">&#9679; REC</span>
                            </div>"""
    new_camera_js = """                            <div class="camera-top-bar">
                                <span>${cam.id} - ${cam.name}</span>
                                <span class="text-high" style="font-size: 11px; display: flex; align-items: center; font-weight: 600;"><span class="rec-dot"></span>REC</span>
                            </div>"""
    html = html.replace(old_camera_js, new_camera_js)

    # 11. Tables alignment in HTML
    old_timeline_th = """                            <tr>
                                <th>Time</th>
                                <th>Cam</th>
                                <th>Type</th>
                                <th>Score</th>
                                <th>Sync</th>
                            </tr>"""
    new_timeline_th = """                            <tr>
                                <th>Time</th>
                                <th>Cam</th>
                                <th>Type</th>
                                <th class="text-right">Score</th>
                                <th class="text-right">Sync</th>
                            </tr>"""
    html = html.replace(old_timeline_th, new_timeline_th)

    old_evidence_th = """                            <tr>
                                <th>EV-ID</th>
                                <th>Time</th>
                                <th>Camera</th>
                                <th>Risk</th>
                                <th>Action</th>
                            </tr>"""
    new_evidence_th = """                            <tr>
                                <th>EV-ID</th>
                                <th>Time</th>
                                <th>Camera</th>
                                <th>Risk</th>
                                <th class="text-right">Action</th>
                            </tr>"""
    html = html.replace(old_evidence_th, new_evidence_th)

    old_anpr_th = """                            <tr>
                                <th>Plate</th>
                                <th>Status</th>
                                <th>Cam</th>
                            </tr>"""
    new_anpr_th = """                            <tr>
                                <th>Plate</th>
                                <th>Status</th>
                                <th class="text-right">Cam</th>
                            </tr>"""
    html = html.replace(old_anpr_th, new_anpr_th)

    # 12. Tables alignment in JS
    old_timeline_tr = """                    <tr>
                        <td class="mono text-muted">${e.timestamp}</td>
                        <td class="mono">${e.camera_id}</td>
                        <td>${e.event_type}</td>
                        <td class="${getTextColor(e.risk_level)} fw-bold">${e.risk_score}</td>
                        <td class="${syncColor} fw-bold" style="font-size: 10px;">${e.sync_status}</td>
                    </tr>"""
    new_timeline_tr = """                    <tr>
                        <td class="mono text-muted">${e.timestamp}</td>
                        <td class="mono">${e.camera_id}</td>
                        <td>${e.event_type}</td>
                        <td class="${getTextColor(e.risk_level)} fw-bold mono text-right">${e.risk_score}</td>
                        <td class="${syncColor} fw-bold text-right" style="font-size: 11px;">${e.sync_status}</td>
                    </tr>"""
    html = html.replace(old_timeline_tr, new_timeline_tr)

    old_evidence_tr = """                    <tr>
                        <td class="mono text-muted">${e.id}</td>
                        <td class="mono text-muted">${e.timestamp}</td>
                        <td class="mono">${e.camera_id}</td>
                        <td><span class="badge ${getBadgeClass(e.risk_level)}">${e.risk_level}</span></td>
                        <td><button class="btn-view">VIEW</button></td>
                    </tr>"""
    new_evidence_tr = """                    <tr>
                        <td class="mono text-muted">${e.id}</td>
                        <td class="mono text-muted">${e.timestamp}</td>
                        <td class="mono">${e.camera_id}</td>
                        <td><span class="badge ${getBadgeClass(e.risk_level)}">${e.risk_level}</span></td>
                        <td class="text-right"><button class="btn-view">VIEW</button></td>
                    </tr>"""
    html = html.replace(old_evidence_tr, new_evidence_tr)

    old_anpr_tr = """                    <tr>
                        <td class="mono font-weight-bold">${a.plate}</td>
                        <td class="${getTextColor(a.status)} fw-bold" style="font-size: 11px;">${a.status}</td>
                        <td class="mono text-muted">${a.camera_id}</td>
                    </tr>"""
    new_anpr_tr = """                    <tr>
                        <td class="mono font-weight-bold">${a.plate}</td>
                        <td class="${getTextColor(a.status)} fw-bold" style="font-size: 11px;">${a.status}</td>
                        <td class="mono text-muted text-right">${a.camera_id}</td>
                    </tr>"""
    html = html.replace(old_anpr_tr, new_anpr_tr)

    # 13. JS logic for Glance update
    old_render_stats = """            function renderStats(stats) {
                els.sumHigh.textContent = stats.high;
                els.sumAtt.textContent = stats.attention;
                els.sumNorm.textContent = stats.normal;
            }"""
    new_render_stats = """            function renderStats(stats) {
                els.sumHigh.textContent = stats.high;
                els.sumAtt.textContent = stats.attention;
                els.sumNorm.textContent = stats.normal;
                
                const glanceHigh = document.getElementById('glance-high-risk');
                if (glanceHigh) glanceHigh.textContent = stats.high;
            }"""
    html = html.replace(old_render_stats, new_render_stats)

    old_render_net = """            function renderNetworkStatus(isOnline, queueLength) {
                if (isOnline) {
                    els.sysNetwork.textContent = 'ONLINE';
                    els.sysNetwork.className = 'text-normal font-weight-bold';
                    els.topNetworkText.textContent = 'NETWORK ONLINE';
                    els.topNetworkText.className = 'text-normal';
                    els.topNetworkDot.className = 'status-dot online';
                    els.sysSync.textContent = '0';
                    els.sysSync.className = 'mono text-muted';
                } else {
                    els.sysNetwork.textContent = 'OFFLINE';
                    els.sysNetwork.className = 'text-high font-weight-bold';
                    els.topNetworkText.textContent = 'NETWORK OFFLINE - LOCAL MODE';
                    els.topNetworkText.className = 'text-high';
                    els.topNetworkDot.className = 'status-dot offline';
                    els.sysSync.textContent = queueLength + ' PENDING';
                    els.sysSync.className = 'mono text-attention';
                }
            }"""
    new_render_net = """            function renderNetworkStatus(isOnline, queueLength) {
                if (isOnline) {
                    els.sysNetwork.textContent = 'ONLINE';
                    els.sysNetwork.className = 'text-normal font-weight-bold';
                    els.topNetworkText.textContent = 'NETWORK ONLINE';
                    els.topNetworkText.className = 'text-normal';
                    els.topNetworkDot.className = 'status-dot online';
                    els.sysSync.textContent = '0';
                    els.sysSync.className = 'mono text-muted';
                } else {
                    els.sysNetwork.textContent = 'OFFLINE';
                    els.sysNetwork.className = 'text-high font-weight-bold';
                    els.topNetworkText.textContent = 'NETWORK OFFLINE - LOCAL MODE';
                    els.topNetworkText.className = 'text-high';
                    els.topNetworkDot.className = 'status-dot offline';
                    els.sysSync.textContent = queueLength + ' PENDING';
                    els.sysSync.className = 'mono text-attention';
                }
                
                const glanceSync = document.getElementById('glance-sync');
                const glanceNet = document.getElementById('glance-network');
                if (glanceSync) glanceSync.textContent = isOnline ? '0' : queueLength;
                if (glanceNet) {
                    if (isOnline) {
                        glanceNet.textContent = 'ONLINE';
                        glanceNet.className = 'glance-value text-normal';
                    } else {
                        glanceNet.textContent = 'OFFLINE';
                        glanceNet.className = 'glance-value text-high';
                    }
                }
            }"""
    html = html.replace(old_render_net, new_render_net)

    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    update_file()
