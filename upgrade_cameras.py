import re

def main():
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update CSS
    old_camera_feed = """        .camera-feed {
            position: relative;
            background-color: #111;
            border: 1px solid var(--border-light);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: inset 0 0 60px rgba(0,0,0,0.9);
            filter: grayscale(15%) contrast(105%);
            border-radius: 4px;
            cursor: pointer;
            transition: border-color 0.2s;
        }
        
        .camera-feed:hover {
            border-color: var(--text-muted);
        }

        /* Fake CCTV noise effect using CSS */
        .camera-noise {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)" opacity="0.08"/%3E%3C/svg%3E');
            pointer-events: none;
            z-index: 1;
        }"""
        
    new_camera_feed = """        .camera-feed {
            position: relative;
            background-color: #111;
            background-size: cover;
            background-position: center;
            border: 1px solid var(--border-light);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: inset 0 0 80px rgba(0,0,0,0.85);
            filter: grayscale(80%) contrast(110%);
            border-radius: 4px;
            cursor: pointer;
            transition: border-color 0.2s;
        }
        
        .camera-feed:hover {
            border-color: var(--text-muted);
        }

        .camera-noise {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.95" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)" opacity="0.12"/%3E%3C/svg%3E');
            pointer-events: none;
            z-index: 1;
        }
        
        .tracks-layer {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: 2;
            pointer-events: none;
            overflow: hidden;
        }"""
    html = html.replace(old_camera_feed, new_camera_feed)
    
    old_bounding_box = """        .bounding-box {
            position: absolute;
            border: 2px solid;
            z-index: 2;
            pointer-events: none;
            display: flex;
            align-items: flex-start;
        }

        .bounding-box .label {
            background-color: inherit;
            color: #000;
            font-size: 10px;
            padding: 2px 6px;
            font-weight: 700;
            margin-top: -18px;
            margin-left: -2px;
            white-space: nowrap;
        }"""
    
    new_bounding_box = """        .bounding-box {
            position: absolute;
            border: 2px solid;
            z-index: 2;
            pointer-events: none;
            display: flex;
            align-items: flex-start;
        }

        .bounding-box .label {
            background-color: inherit;
            color: #000;
            font-size: 10px;
            padding: 2px 6px;
            font-weight: 700;
            margin-top: -18px;
            margin-left: -2px;
            white-space: nowrap;
            text-shadow: none;
        }"""
    html = html.replace(old_bounding_box, new_bounding_box)

    # Replace entire <script> block with new logic
    script_start = html.find('<script>')
    script_end = html.find('</script>') + 9
    
    new_script = """<script>
        const SVGS = {
            'C01': `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="%232a2a2a"/><rect y="200" width="400" height="100" fill="%233a3a3a"/><line x1="0" y1="200" x2="400" y2="200" stroke="%23111" stroke-width="4"/><path d="M50,150 v150 M150,150 v150 M250,150 v150 M350,150 v150 M0,180 h400 M0,210 h400" stroke="%23111" stroke-width="2" opacity="0.6"/></svg>`,
            'C02': `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="%23252525"/><path d="M150,300 L180,180 L220,180 L250,300 Z" fill="%23333"/><rect x="80" y="160" width="20" height="140" fill="%23111"/><rect x="300" y="160" width="20" height="140" fill="%23111"/><rect x="80" y="180" width="120" height="10" fill="%23111"/></svg>`,
            'C03': `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="%232d2d2d"/><path d="M0,300 L180,150 L220,150 L400,300 Z" fill="%233a3a3a"/><line x1="200" y1="150" x2="200" y2="300" stroke="%23444" stroke-width="2" stroke-dasharray="10,10"/></svg>`,
            'C04': `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="%23222"/><rect y="100" width="400" height="200" fill="%23333"/><polygon points="80,150 320,150 360,280 40,280" fill="none" stroke="%23f59e0b" stroke-width="2" stroke-dasharray="8,4" opacity="0.5"/></svg>`,
            'C05': `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="%232a2a2a"/><rect y="180" width="400" height="120" fill="%233a3a3a"/><path d="M50,180 Q60,150 70,180 M150,180 Q170,140 190,180 M300,180 Q320,130 340,180" fill="%23111"/></svg>`,
            'C06': `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="%231e293b"/><rect y="160" width="400" height="140" fill="%23334155"/><path d="M100,160 Q150,100 200,160 T300,160" fill="none" stroke="%2394a3b8" stroke-width="2" opacity="0.4"/></svg>`
        };

        const DataSim = (function() {
            let state = {
                networkOnline: true,
                syncQueue: [],
                events: [],
                cameras: [
                    { id: 'C01', name: 'North Fence', status: 'ONLINE', fps: 24, tracks: [] },
                    { id: 'C02', name: 'Vehicle Gate', status: 'ONLINE', fps: 30, tracks: [] },
                    { id: 'C03', name: 'Patrol Road', status: 'ONLINE', fps: 24, tracks: [] },
                    { id: 'C04', name: 'Restricted Zone', status: 'ONLINE', fps: 15, tracks: [] },
                    { id: 'C05', name: 'East Perimeter', status: 'ONLINE', fps: 24, tracks: [] },
                    { id: 'C06', name: 'Thermal Overview', status: 'ONLINE', fps: 9, tracks: [] }
                ],
                evidence: [],
                anpr: [],
                stats: { high: 14, attention: 42, normal: 342 }
            };

            const EVENT_TYPES = [
                { type: 'Perimeter Breach', risk_level: 'HIGH', base_score: 90 },
                { type: 'Restricted Zone Crossing', risk_level: 'HIGH', base_score: 85 },
                { type: 'Loitering > 60s', risk_level: 'ATTENTION', base_score: 65 },
                { type: 'Unidentified Vehicle', risk_level: 'ATTENTION', base_score: 70 },
                { type: 'Person Detected', risk_level: 'NORMAL', base_score: 30 },
                { type: 'Vehicle Detected', risk_level: 'NORMAL', base_score: 25 },
                { type: 'Wildlife Detected', risk_level: 'NORMAL', base_score: 10 }
            ];

            const PLATES = ['ABC-1234', 'XYZ-9876', 'GVT-001', 'UNK-????', 'TRK-5542'];

            let eventCounter = 10000;
            let evidenceCounter = 5000;

            function generateId() {
                return 'TRK-' + Math.floor(Math.random() * 10000).toString().padStart(4, '0');
            }

            function generateTimestamp() {
                const now = new Date();
                return now.toISOString().split('T')[1].split('.')[0];
            }

            function triggerEvent() {
                const cam = state.cameras[Math.floor(Math.random() * state.cameras.length)];
                
                const rand = Math.random();
                let eventDef;
                if (rand > 0.95) eventDef = EVENT_TYPES[0];
                else if (rand > 0.90) eventDef = EVENT_TYPES[1];
                else if (rand > 0.80) eventDef = EVENT_TYPES[2];
                else if (rand > 0.70) eventDef = EVENT_TYPES[3];
                else if (rand > 0.40) eventDef = EVENT_TYPES[4];
                else if (rand > 0.20) eventDef = EVENT_TYPES[5];
                else eventDef = EVENT_TYPES[6];

                const risk_score = Math.min(99, eventDef.base_score + Math.floor(Math.random() * 15));
                
                const event = {
                    id: 'EVT-' + (++eventCounter),
                    track_id: generateId(),
                    camera_id: cam.id,
                    event_type: eventDef.type,
                    risk_score: risk_score,
                    risk_level: eventDef.risk_level,
                    timestamp: generateTimestamp(),
                    duration: Math.floor(Math.random() * 120) + 's',
                    sync_status: state.networkOnline ? 'SYNCED' : 'PENDING'
                };

                state.events.unshift(event);
                if (state.events.length > 50) state.events.pop();

                if (!state.networkOnline) {
                    state.syncQueue.push(event.id);
                }

                if (event.risk_level === 'HIGH') state.stats.high++;
                else if (event.risk_level === 'ATTENTION') state.stats.attention++;
                else state.stats.normal++;

                if (event.risk_level === 'HIGH' || (event.risk_level === 'ATTENTION' && Math.random() > 0.5)) {
                    state.evidence.unshift({
                        id: 'EVD-' + (++evidenceCounter),
                        camera_id: event.camera_id,
                        timestamp: event.timestamp,
                        risk_level: event.risk_level,
                        ref_event: event.id
                    });
                    if (state.evidence.length > 20) state.evidence.pop();
                }

                if (event.event_type.includes('Vehicle') && (cam.id === 'C02' || cam.id === 'C03')) {
                    const plate = PLATES[Math.floor(Math.random() * PLATES.length)];
                    const status = plate.includes('UNK') ? 'UNKNOWN' : (Math.random() > 0.2 ? 'AUTHORIZED' : 'FLAGGED');
                    state.anpr.unshift({
                        plate: plate,
                        camera_id: cam.id,
                        timestamp: event.timestamp,
                        status: status,
                        confidence: Math.floor(80 + Math.random() * 19) + '%'
                    });
                    if (state.anpr.length > 20) state.anpr.pop();
                }
                
                if (window.UIHandler) window.UIHandler.onDataUpdate();
            }

            function toggleNetwork() {
                state.networkOnline = !state.networkOnline;
                if (state.networkOnline) {
                    state.events.forEach(e => {
                        if (e.sync_status === 'PENDING') e.sync_status = 'SYNCED';
                    });
                    state.syncQueue = [];
                }
                if (window.UIHandler) window.UIHandler.onDataUpdate();
                return state.networkOnline;
            }

            // Tracking simulation loop
            setInterval(() => {
                const now = Date.now();
                let tracksChanged = false;
                
                state.cameras.forEach(cam => {
                    if (!cam.tracks) cam.tracks = [];
                    
                    // Remove expired tracks
                    const initialLen = cam.tracks.length;
                    cam.tracks = cam.tracks.filter(t => now - t.startTs < t.duration);
                    if (cam.tracks.length !== initialLen) tracksChanged = true;
                    
                    // Update specific logic (C04 zone crossing)
                    if (cam.id === 'C04') {
                        cam.tracks.forEach(t => {
                            const progress = (now - t.startTs) / t.duration;
                            const curX = t.startX + (t.endX - t.startX) * progress;
                            const curY = t.startY + (t.endY - t.startY) * progress;
                            // Zone roughly 20% to 90% X, 50% to 93% Y
                            if (curX > 20 && curX < 90 && curY > 50 && curY < 93) {
                                if (t.color === 'var(--risk-normal)') {
                                    t.color = 'var(--risk-attention)'; // amber
                                    tracksChanged = true;
                                }
                            }
                        });
                    }
                    
                    // Randomly add new tracks
                    if (cam.tracks.length < 3 && Math.random() > 0.7) {
                        const isPerson = Math.random() > 0.5;
                        const cls = isPerson ? 'person' : 'vehicle';
                        const conf = (0.80 + Math.random() * 0.19).toFixed(2);
                        const idNum = Math.floor(Math.random() * 100);
                        const label = `ID:${idNum} ${cls} ${conf}`;
                        
                        const isHighRisk = Math.random() > 0.95;
                        const baseColor = isHighRisk ? 'var(--risk-high)' : 'var(--risk-normal)';
                        
                        // spawn left or right
                        const startX = Math.random() > 0.5 ? -15 : 100;
                        const endX = startX < 0 ? 100 : -15;
                        const startY = 30 + Math.random() * 40;
                        const endY = startY + (Math.random() * 20 - 10);
                        
                        cam.tracks.push({
                            id: Math.random().toString(36).substr(2, 9),
                            label,
                            startX, startY, endX, endY,
                            w: isPerson ? 6 : 14,
                            h: isPerson ? 18 : 12,
                            duration: 4000 + Math.random() * 3000,
                            color: baseColor,
                            startTs: now
                        });
                        tracksChanged = true;
                    }
                });
                
                if (tracksChanged && window.UIHandler) {
                    window.UIHandler.onTracksUpdate();
                }
                
            }, 500);

            setInterval(() => {
                if (Math.random() > 0.4) triggerEvent();
            }, 3000);

            setInterval(() => {
                if (window.UIHandler) window.UIHandler.updateHardwareStats();
            }, 2000);

            for(let i=0; i<15; i++) triggerEvent();

            return {
                getState: () => state,
                toggleNetwork: toggleNetwork
            };
        })();

        window.UIHandler = (function() {
            // Sidebar Navigation Logic
            const navItems = document.querySelectorAll('.nav-item');
            const pageViews = document.querySelectorAll('.page-view');

            navItems.forEach(item => {
                item.addEventListener('click', () => {
                    navItems.forEach(nav => nav.classList.remove('active'));
                    item.classList.add('active');
                    
                    const targetPageId = 'page-' + item.getAttribute('data-target');
                    pageViews.forEach(page => {
                        if(page.id === targetPageId) {
                            page.classList.add('active');
                        } else {
                            page.classList.remove('active');
                        }
                    });
                });
            });

            const els = {
                clock: document.getElementById('clock-display'),
                camerasOverview: document.getElementById('camera-grid-overview'),
                camerasFull: document.getElementById('camera-grid-full'),
                alerts: document.getElementById('alerts-list'),
                timeline: document.getElementById('timeline-body'),
                evidence: document.getElementById('evidence-body'),
                anpr: document.getElementById('anpr-body'),
                sysNetwork: document.getElementById('sys-network'),
                topNetworkDot: document.getElementById('top-network-dot'),
                topNetworkText: document.getElementById('top-network-text'),
                sysSync: document.getElementById('sys-sync'),
                btnOffline: document.getElementById('demo-offline-btn'),
                sumHigh: document.getElementById('sum-high'),
                sumAtt: document.getElementById('sum-att'),
                sumNorm: document.getElementById('sum-norm'),
                meterCpu: document.getElementById('meter-cpu'),
                meterCpuVal: document.getElementById('meter-cpu-val'),
                meterGpu: document.getElementById('meter-gpu'),
                meterGpuVal: document.getElementById('meter-gpu-val'),
                meterRam: document.getElementById('meter-ram'),
                meterRamVal: document.getElementById('meter-ram-val'),
                meterSto: document.getElementById('meter-sto'),
                meterStoVal: document.getElementById('meter-sto-val')
            };

            function updateClock() {
                const now = new Date();
                els.clock.textContent = now.toISOString().split('T')[0] + ' ' + now.toTimeString().split(' ')[0];
            }
            setInterval(updateClock, 1000);
            updateClock();

            els.btnOffline.addEventListener('click', () => {
                const isOnline = DataSim.toggleNetwork();
                if (isOnline) {
                    els.btnOffline.textContent = 'Simulate Offline';
                    els.btnOffline.classList.remove('active');
                } else {
                    els.btnOffline.textContent = 'Reconnect';
                    els.btnOffline.classList.add('active');
                }
            });

            function getBadgeClass(level) {
                if (level === 'HIGH') return 'badge-high';
                if (level === 'ATTENTION') return 'badge-attention';
                return 'badge-normal';
            }

            function getTextColor(level) {
                if (level === 'HIGH') return 'text-high';
                if (level === 'ATTENTION') return 'text-attention';
                if (level === 'FLAGGED') return 'text-high';
                if (level === 'UNKNOWN') return 'text-attention';
                return 'text-normal';
            }

            function generateCameraHTML(cameras) {
                let html = '';
                if (!document.getElementById('blink-anim')) {
                    const style = document.createElement('style');
                    style.id = 'blink-anim';
                    style.innerHTML = `@keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }`;
                    document.head.appendChild(style);
                }

                cameras.forEach(cam => {
                    const bgUrl = SVGS[cam.id] || SVGS['C01'];
                    const curFps = cam.fps - Math.floor(Math.random() * 2);

                    html += `
                    <div class="camera-feed" data-cam="${cam.id}" style="background-image: url('${bgUrl}');">
                        <div class="camera-noise"></div>
                        <div class="tracks-layer"></div>
                        <div class="camera-overlay">
                            <div class="camera-top-bar">
                                <span>${cam.id} - ${cam.name}</span>
                                <span class="text-high" style="font-size: 11px; display: flex; align-items: center; font-weight: 600;"><span class="rec-dot"></span>REC</span>
                            </div>
                            <div class="camera-bottom-bar">
                                <span>${els.clock.textContent.split(' ')[1] || '00:00:00'}</span>
                                <span class="fps-det-label">${curFps} FPS | DET: <span class="det-count">0</span></span>
                            </div>
                        </div>
                    </div>`;
                });
                return html;
            }

            let camerasRendered = false;

            function renderCameras(cameras) {
                if (!camerasRendered) {
                    const camHtml = generateCameraHTML(cameras);
                    els.camerasOverview.innerHTML = camHtml;
                    els.camerasFull.innerHTML = camHtml;
                    camerasRendered = true;
                }
            }

            function onTracksUpdate() {
                const state = DataSim.getState();
                state.cameras.forEach(cam => {
                    const containers = document.querySelectorAll(`.camera-feed[data-cam="${cam.id}"]`);
                    
                    containers.forEach(container => {
                        const layer = container.querySelector('.tracks-layer');
                        if (!layer) return;
                        
                        // Update detection count
                        const detCount = container.querySelector('.det-count');
                        if (detCount) detCount.textContent = cam.tracks.length;

                        const existingIds = Array.from(layer.children).map(c => c.id);
                        const currentIds = cam.tracks.map(t => 'box-' + t.id);
                        
                        // Remove expired
                        existingIds.forEach(id => {
                            if (!currentIds.includes(id)) {
                                layer.querySelector('#'+id).remove();
                            }
                        });
                        
                        // Add or update
                        cam.tracks.forEach(t => {
                            const elId = 'box-' + t.id;
                            let el = layer.querySelector('#'+elId);
                            if (!el) {
                                el = document.createElement('div');
                                el.id = elId;
                                el.className = 'bounding-box';
                                el.innerHTML = `<div class="label" style="background-color: ${t.color}">${t.label}</div>`;
                                el.style.left = t.startX + '%';
                                el.style.top = t.startY + '%';
                                el.style.width = t.w + '%';
                                el.style.height = t.h + '%';
                                el.style.borderColor = t.color;
                                // Add to DOM
                                layer.appendChild(el);
                                
                                // Force reflow then start transition to target
                                requestAnimationFrame(() => {
                                    requestAnimationFrame(() => {
                                        el.style.transition = `left ${t.duration}ms linear, top ${t.duration}ms linear, border-color 0.5s`;
                                        el.style.left = t.endX + '%';
                                        el.style.top = t.endY + '%';
                                    });
                                });
                            } else {
                                // Dynamic color update (e.g. entering zone)
                                if (el.style.borderColor !== t.color) {
                                    el.style.borderColor = t.color;
                                    el.querySelector('.label').style.backgroundColor = t.color;
                                }
                            }
                        });
                    });
                });
            }

            function renderAlerts(events) {
                const alerts = events.filter(e => e.risk_level !== 'NORMAL').slice(0, 3);
                let html = '';
                alerts.forEach(a => {
                    html += `
                    <div class="list-item">
                        <div class="list-item-header">
                            <span class="badge ${getBadgeClass(a.risk_level)}">${a.risk_level}</span>
                            <span class="mono text-muted" style="font-size: 11px;">${a.timestamp}</span>
                        </div>
                        <div style="font-weight: 600; font-size: 13px; margin-top: 4px;">${a.event_type}</div>
                        <div class="list-item-body">
                            <span class="mono">CAM: ${a.camera_id}</span>
                            <span>SCORE: <span class="${getTextColor(a.risk_level)} fw-bold">${a.risk_score}</span></span>
                        </div>
                    </div>`;
                });
                els.alerts.innerHTML = html;
            }

            function renderTimeline(events) {
                let html = '';
                events.forEach(e => {
                    const syncColor = e.sync_status === 'SYNCED' ? 'text-normal' : 'text-attention';
                    html += `
                    <tr>
                        <td class="mono text-muted">${e.timestamp}</td>
                        <td class="mono">${e.camera_id}</td>
                        <td>${e.event_type}</td>
                        <td class="${getTextColor(e.risk_level)} fw-bold mono text-right">${e.risk_score}</td>
                        <td class="${syncColor} fw-bold text-right" style="font-size: 11px;">${e.sync_status}</td>
                    </tr>`;
                });
                els.timeline.innerHTML = html;
            }

            function renderEvidence(evidence) {
                let html = '';
                evidence.forEach(e => {
                    html += `
                    <tr>
                        <td class="mono text-muted" title="${e.id}">${e.id}</td>
                        <td class="mono text-muted">${e.timestamp}</td>
                        <td class="mono">${e.camera_id}</td>
                        <td><span class="badge ${getBadgeClass(e.risk_level)}">${e.risk_level}</span></td>
                        <td class="text-right"><button class="btn-view">VIEW</button></td>
                    </tr>`;
                });
                els.evidence.innerHTML = html;
            }

            function renderANPR(anpr) {
                let html = '';
                anpr.forEach(a => {
                    html += `
                    <tr>
                        <td class="mono font-weight-bold">${a.plate}</td>
                        <td class="${getTextColor(a.status)} fw-bold" style="font-size: 11px;">${a.status}</td>
                        <td class="mono text-muted text-right">${a.camera_id}</td>
                    </tr>`;
                });
                els.anpr.innerHTML = html;
            }

            function renderStats(stats) {
                els.sumHigh.textContent = stats.high;
                els.sumAtt.textContent = stats.attention;
                els.sumNorm.textContent = stats.normal;
                
                const glanceHigh = document.getElementById('glance-high-risk');
                if (glanceHigh) glanceHigh.textContent = stats.high;
            }

            function renderNetworkStatus(isOnline, queueLength) {
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
            }

            function updateHardwareStats() {
                const cpu = 35 + Math.floor(Math.random() * 15);
                const gpu = 70 + Math.floor(Math.random() * 20);
                const ram = 11.5 + (Math.random() * 1.5);
                
                if(els.meterCpuVal) {
                    els.meterCpuVal.textContent = cpu + '%';
                    els.meterCpu.style.width = cpu + '%';
                }
                
                if(els.meterGpuVal) {
                    els.meterGpuVal.textContent = gpu + '%';
                    els.meterGpu.style.width = gpu + '%';
                    if (gpu > 85) els.meterGpu.className = 'meter-bar-fill crit';
                    else els.meterGpu.className = 'meter-bar-fill warn';
                }

                if(els.meterRamVal) {
                    els.meterRamVal.textContent = ram.toFixed(1) + 'GB / 16GB';
                    const ramPct = (ram / 16) * 100;
                    els.meterRam.style.width = ramPct + '%';
                }
            }

            function onDataUpdate() {
                const state = DataSim.getState();
                renderCameras(state.cameras);
                renderAlerts(state.events);
                renderTimeline(state.events);
                renderEvidence(state.evidence);
                renderANPR(state.anpr);
                renderStats(state.stats);
                renderNetworkStatus(state.networkOnline, state.syncQueue.length);
            }

            // Initial render
            onDataUpdate();

            return {
                onDataUpdate,
                onTracksUpdate,
                updateHardwareStats
            };
        })();
    </script>"""
    
    html = html[:script_start] + new_script + html[script_end:]
    
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    main()
