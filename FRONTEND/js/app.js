/**
 * Cloud Gaming Optimizer - Dashboard JavaScript
 * Real-time updates and interactive charts
 */

// Configuration
const CONFIG = {
    refreshInterval: 2000, // 2 seconds
    historyLength: 60,     // 60 data points for charts
    apiEndpoints: {
        metrics: '/api/metrics',
        optimize: '/api/optimize',
        alerts: '/api/alerts',
        stats: '/api/stats'
    }
};

// State
let networkHistory = {
    labels: [],
    latency: [],
    jitter: [],
    packetLoss: []
};

let systemHistory = {
    labels: [],
    cpu: [],
    ram: [],
    gpu: []
};

let scoreHistory = {
    labels: [],
    scores: []
};

// Initialize charts when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    detectDevice();
    startRealTimeUpdates();
});

// Chart instances
let networkChart, systemChart, scoreChart;

/**
 * Initialize all charts
 */
function initializeCharts() {
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 300
        },
        plugins: {
            legend: {
                labels: {
                    color: '#94a3b8'
                }
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(51, 65, 85, 0.5)'
                },
                ticks: {
                    color: '#64748b'
                }
            },
            y: {
                grid: {
                    color: 'rgba(51, 65, 85, 0.5)'
                },
                ticks: {
                    color: '#64748b'
                }
            }
        }
    };

    // Network Chart
    const networkCtx = document.getElementById('networkChart').getContext('2d');
    networkChart = new Chart(networkCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Latency (ms)',
                    data: [],
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Jitter (ms)',
                    data: [],
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: chartOptions
    });

    // System Chart
    const systemCtx = document.getElementById('systemChart').getContext('2d');
    systemChart = new Chart(systemCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'CPU %',
                    data: [],
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'RAM %',
                    data: [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'GPU %',
                    data: [],
                    borderColor: '#f97316',
                    backgroundColor: 'rgba(249, 115, 22, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: chartOptions
    });

    // Score Chart
    const scoreCtx = document.getElementById('scoreChart').getContext('2d');
    scoreChart = new Chart(scoreCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Performance Score',
                data: [],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            ...chartOptions,
            scales: {
                ...chartOptions.scales,
                y: {
                    ...chartOptions.scales.y,
                    min: 0,
                    max: 100
                }
            }
        }
    });
}

/**
 * Start real-time updates
 */
function startRealTimeUpdates() {
    updateAllData();
    setInterval(updateAllData, CONFIG.refreshInterval);
}

/**
 * Update all data from API
 */
async function updateAllData() {
    try {
        const [metricsData, optimizeData, alertsData] = await Promise.all([
            fetch(CONFIG.apiEndpoints.metrics).then(r => r.json()),
            fetch(CONFIG.apiEndpoints.optimize).then(r => r.json()),
            fetch(CONFIG.apiEndpoints.alerts).then(r => r.json())
        ]);

        if (metricsData.success) {
            updateMetricsDisplay(metricsData);
            updateCharts(metricsData);
            updateHealthBanner(metricsData.system_health);
        }

        if (optimizeData.success) {
            updateOptimization(optimizeData);
        }

        if (alertsData.success) {
            updateAlerts(alertsData);
        }

        updateLastUpdateTime();
        setConnectionStatus(true);
    } catch (error) {
        console.error('Error updating data:', error);
        setConnectionStatus(false);
    }
}

/**
 * Update metrics display
 */
function updateMetricsDisplay(data) {
    const network = data.network;
    const system = data.system;

    // Network Metrics
    updateMetricValue('latencyValue', network.ping_ms, 'ms');
    updateMetricValue('jitterValue', network.jitter_ms, 'ms');
    updateMetricValue('packetLossValue', network.packet_loss_percent, '%');

    // Network bars (scale: 0-200ms for latency, 0-100ms for jitter, 0-20% for packet loss)
    updateMetricBar('latencyBar', network.ping_ms, 200);
    updateMetricBar('jitterBar', network.jitter_ms, 100);
    updateMetricBar('packetLossBar', network.packet_loss_percent, 20);

    // System Metrics
    updateMetricValue('cpuValue', system.cpu_percent, '%');
    updateMetricValue('ramValue', system.ram_percent, '%');
    updateMetricValue('gpuValue', system.gpu_available ? system.gpu_percent : '-', '%');
    updateMetricValue('diskValue', system.disk_percent, '%');

    // System bars
    updateMetricBar('cpuBar', system.cpu_percent, 100);
    updateMetricBar('ramBar', system.ram_percent, 100);
    updateMetricBar('gpuBar', system.gpu_percent, 100);
    updateMetricBar('diskBar', system.disk_percent, 100);

    // System details
    document.getElementById('cpuCores').textContent = system.cpu_count || '--';
    document.getElementById('cpuFreq').textContent = system.cpu_freq_ghz || '--';
    document.getElementById('ramUsed').textContent = system.ram_used_gb || '--';
    document.getElementById('ramTotal').textContent = system.ram_total_gb || '--';
    document.getElementById('gpuName').textContent = system.gpu_name || 'N/A';
    document.getElementById('gpuMemory').textContent = system.gpu_memory_percent || '--';
    document.getElementById('diskUsed').textContent = system.disk_used_gb || '--';
    document.getElementById('diskTotal').textContent = system.disk_total_gb || '--';

    // Badges
    updateBadge('cpuBadge', system.cpu_percent);
    updateBadge('ramBadge', system.ram_percent);
    updateBadge('gpuBadge', system.gpu_percent);
    updateBadge('diskBadge', system.disk_percent);
}

/**
 * Update a metric value element
 */
function updateMetricValue(elementId, value, unit) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = typeof value === 'number' ? value.toFixed(1) : value;
    }
}

/**
 * Update a metric bar with color based on value
 */
function updateMetricBar(barId, value, max) {
    const bar = document.getElementById(barId);
    if (bar) {
        const percentage = Math.min((value / max) * 100, 100);
        bar.style.width = percentage + '%';

        // Remove old classes
        bar.classList.remove('warning', 'danger');

        // Add appropriate class based on threshold
        if (percentage >= 80) {
            bar.classList.add('danger');
        } else if (percentage >= 60) {
            bar.classList.add('warning');
        }
    }
}

/**
 * Update badge with color based on value
 */
function updateBadge(badgeId, value) {
    const badge = document.getElementById(badgeId);
    if (badge) {
        badge.textContent = typeof value === 'number' ? value.toFixed(0) + '%' : value;
        badge.classList.remove('warning', 'critical');

        if (value >= 90) {
            badge.classList.add('critical');
        } else if (value >= 75) {
            badge.classList.add('warning');
        }
    }
}

/**
 * Update health banner
 */
function updateHealthBanner(health) {
    const banner = document.getElementById('healthBanner');
    const status = document.getElementById('healthStatus');

    banner.classList.remove('warning', 'critical');

    if (health && health.overall_status) {
        status.textContent = `System Health: ${health.overall_status}`;

        if (health.overall_status === 'Critical') {
            banner.classList.add('critical');
        } else if (health.overall_status === 'Warning') {
            banner.classList.add('warning');
        }
    }
}

/**
 * Update optimization recommendations
 */
function updateOptimization(data) {
    const rec = data.recommendations;

    document.getElementById('recResolution').textContent = rec.resolution || '--';
    document.getElementById('recFps').textContent = rec.fps ? rec.fps + ' FPS' : '--';
    document.getElementById('recBitrate').textContent = rec.bitrate_mbps ? rec.bitrate_mbps + ' Mbps' : '--';
    document.getElementById('recPriority').textContent = rec.priority || '--';
    document.getElementById('optReason').textContent = data.optimization_reason || 'Analyzing...';
}

/**
 * Update alerts display
 */
function updateAlerts(data) {
    const container = document.getElementById('alertsContainer');
    const noAlerts = document.getElementById('noAlerts');
    const alertCount = document.getElementById('alertCount');

    alertCount.textContent = data.alert_count || 0;

    // Clear existing alerts (except no-alerts message)
    const existingAlerts = container.querySelectorAll('.alert-item');
    existingAlerts.forEach(alert => alert.remove());

    if (data.alerts && data.alerts.length > 0) {
        noAlerts.style.display = 'none';

        // Show last 5 alerts
        data.alerts.slice(0, 5).forEach(alert => {
            const alertEl = document.createElement('div');
            alertEl.className = `alert-item ${alert.level.toLowerCase()}`;

            let icon = 'info-circle';
            if (alert.level === 'WARNING') icon = 'exclamation-triangle';
            if (alert.level === 'CRITICAL') icon = 'times-circle';

            alertEl.innerHTML = `
                <i class="fas fa-${icon} alert-icon"></i>
                <div class="alert-content">
                    <div class="alert-message">${alert.message}</div>
                    <div class="alert-meta">${alert.metric} | Threshold: ${alert.threshold}</div>
                </div>
            `;

            container.appendChild(alertEl);
        });
    } else {
        noAlerts.style.display = 'flex';
    }
}

/**
 * Update charts with new data
 */
function updateCharts(data) {
    const now = new Date().toLocaleTimeString();
    const network = data.network;
    const system = data.system;

    // Update network history
    if (networkHistory.labels.length >= CONFIG.historyLength) {
        networkHistory.labels.shift();
        networkHistory.latency.shift();
        networkHistory.jitter.shift();
        networkHistory.packetLoss.shift();
    }
    networkHistory.labels.push(now);
    networkHistory.latency.push(network.ping_ms);
    networkHistory.jitter.push(network.jitter_ms);
    networkHistory.packetLoss.push(network.packet_loss_percent);

    // Update network chart
    networkChart.data.labels = networkHistory.labels;
    networkChart.data.datasets[0].data = networkHistory.latency;
    networkChart.data.datasets[1].data = networkHistory.jitter;
    networkChart.update('none');

    // Update system history
    if (systemHistory.labels.length >= CONFIG.historyLength) {
        systemHistory.labels.shift();
        systemHistory.cpu.shift();
        systemHistory.ram.shift();
        systemHistory.gpu.shift();
    }
    systemHistory.labels.push(now);
    systemHistory.cpu.push(system.cpu_percent);
    systemHistory.ram.push(system.ram_percent);
    systemHistory.gpu.push(system.gpu_percent);

    // Update system chart
    systemChart.data.labels = systemHistory.labels;
    systemChart.data.datasets[0].data = systemHistory.cpu;
    systemChart.data.datasets[1].data = systemHistory.ram;
    systemChart.data.datasets[2].data = systemHistory.gpu;
    systemChart.update('none');

    // Calculate and update performance score
    const score = calculatePerformanceScore(network, system);

    if (scoreHistory.labels.length >= CONFIG.historyLength) {
        scoreHistory.labels.shift();
        scoreHistory.scores.shift();
    }
    scoreHistory.labels.push(now);
    scoreHistory.scores.push(score);

    scoreChart.data.labels = scoreHistory.labels;
    scoreChart.data.datasets[0].data = scoreHistory.scores;
    scoreChart.update('none');
}

/**
 * Calculate performance score based on metrics
 */
function calculatePerformanceScore(network, system) {
    let score = 100;

    // Latency penalty (0-50ms = no penalty, 50-100ms = small, >100ms = large)
    if (network.ping_ms > 50) {
        score -= Math.min((network.ping_ms - 50) * 0.3, 25);
    }

    // Jitter penalty
    if (network.jitter_ms > 10) {
        score -= Math.min((network.jitter_ms - 10) * 0.5, 15);
    }

    // Packet loss penalty
    score -= network.packet_loss_percent * 2;

    // CPU penalty
    if (system.cpu_percent > 70) {
        score -= (system.cpu_percent - 70) * 0.3;
    }

    // RAM penalty
    if (system.ram_percent > 80) {
        score -= (system.ram_percent - 80) * 0.5;
    }

    // GPU penalty (if available)
    if (system.gpu_available && system.gpu_percent > 85) {
        score -= (system.gpu_percent - 85) * 0.4;
    }

    return Math.max(0, Math.min(100, Math.round(score)));
}

/**
 * Update last update time
 */
function updateLastUpdateTime() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString();
    document.getElementById('lastUpdate').textContent = `Last update: ${timeStr}`;
}

/**
 * Set connection status
 */
function setConnectionStatus(connected) {
    const status = document.getElementById('connectionStatus');
    if (connected) {
        status.classList.remove('disconnected');
        status.querySelector('i').classList.add('fa-circle');
        status.querySelector('span:last-child').textContent = 'Connected';
    } else {
        status.classList.add('disconnected');
        status.querySelector('span:last-child').textContent = 'Disconnected';
    }
}

/**
 * Detect client device information using available browser APIs
 * Note: Browsers limit exact hardware/vendor exposure for privacy.
 */
function detectDevice() {
    const ua = navigator.userAgent || '';
    const platform = navigator.platform || (navigator.userAgentData && navigator.userAgentData.platform) || 'Unknown';
    const cores = navigator.hardwareConcurrency || 'Unknown';
    const memory = navigator.deviceMemory ? navigator.deviceMemory + ' GB' : 'Unknown';
    const resolution = (screen && screen.width) ? `${screen.width} x ${screen.height}` : 'Unknown';
    const isMobileUA = /Mobi|Android|iPhone|iPad|iPod|Mobile/i.test(ua) || (navigator.userAgentData && navigator.userAgentData.mobile);
    const deviceType = isMobileUA ? 'Mobile' : 'Desktop';

    // Try to get higher-entropy details when supported
    // First, use client-side heuristics
    const clientSideName = parseDeviceFromUA(ua) || (navigator.userAgentData && navigator.userAgentData.brands && navigator.userAgentData.brands[0] && navigator.userAgentData.brands[0].brand) || platform;

    if (navigator.userAgentData && navigator.userAgentData.getHighEntropyValues) {
        navigator.userAgentData.getHighEntropyValues(['model', 'platform', 'architecture']).then(info => {
            const name = info.model || clientSideName;
            displayDeviceInfo({ ua, platform: info.platform || platform, cores, memory, resolution, type: deviceType, name });
            // After displaying client-side info, fetch server-side hints and merge
            fetchAndMergeServerHints();
        }).catch(() => {
            displayDeviceInfo({ ua, platform, cores, memory, resolution, type: deviceType, name: clientSideName });
            fetchAndMergeServerHints();
        });
    } else {
        displayDeviceInfo({ ua, platform, cores, memory, resolution, type: deviceType, name: clientSideName });
        fetchAndMergeServerHints();
    }
}

// Fetch server-observed client hints and merge into UI when available
function fetchAndMergeServerHints() {
    fetch('/api/client_hints').then(r => r.json()).then(payload => {
        if (!payload || !payload.success) return;
        const hints = payload.hints || {};

        // Prefer server-provided model/platform when present
        const serverModel = hints.sec_ch_ua_model || null;
        const serverPlatform = hints.sec_ch_ua_platform || null;

        const currentName = document.getElementById('deviceName').textContent;
        const nameToShow = serverModel || currentName;
        if (nameToShow) document.getElementById('deviceName').textContent = nameToShow;

        if (serverPlatform) document.getElementById('devicePlatform').textContent = serverPlatform;

        // If detection still seems insufficient, show fallback prompt
        const isUnknown = !nameToShow || nameToShow === 'Unknown' || nameToShow === '--';
        handleFallbackPrompt(isUnknown);
    }).catch(() => {
        // If server call fails, still allow fallback prompt based on client detection
        const name = document.getElementById('deviceName').textContent;
        const isUnknown = !name || name === 'Unknown' || name === '--';
        handleFallbackPrompt(isUnknown);
    });
}

function handleFallbackPrompt(show) {
    const stored = localStorage.getItem('reportedDevice');
    const prompt = document.getElementById('deviceFallbackPrompt');
    if (stored) {
        // If user provided a device earlier, use it
        document.getElementById('deviceName').textContent = stored;
        if (prompt) prompt.style.display = 'none';
        return;
    }

    if (show && prompt) {
        prompt.style.display = 'flex';
        const input = document.getElementById('deviceManualInput');
        const save = document.getElementById('deviceManualSave');
        const dismiss = document.getElementById('deviceManualDismiss');

        if (save && input) save.onclick = () => {
            const v = input.value.trim();
            if (!v) return;
            localStorage.setItem('reportedDevice', v);
            document.getElementById('deviceName').textContent = v;
            prompt.style.display = 'none';
        };

        if (dismiss) dismiss.onclick = () => { prompt.style.display = 'none'; };
    } else if (prompt) {
        prompt.style.display = 'none';
    }
}

function parseDeviceFromUA(ua) {
    // Android often includes the model in parentheses: "(Linux; Android 11; SM-G991B)"
    const androidMatch = ua.match(/Android[^;]*;\s*([^;\)]+)\)/i);
    if (androidMatch && androidMatch[1]) return androidMatch[1].trim();

    // iPhone/iPad
    if (/iPad|iPhone|iPod/.test(ua)) {
        const m = ua.match(/iPhone|iPad|iPod/);
        return m ? m[0] : null;
    }

    // Desktops and laptops rarely expose vendor/model in UA; return null to fall back to platform
    return null;
}

function displayDeviceInfo(info) {
    const nameEl = document.getElementById('deviceName');
    const platformEl = document.getElementById('devicePlatform');
    const uaEl = document.getElementById('deviceUA');
    const coresEl = document.getElementById('deviceCores');
    const memoryEl = document.getElementById('deviceMemory');
    const resEl = document.getElementById('deviceResolution');
    const typeEl = document.getElementById('deviceType');

    if (nameEl) nameEl.textContent = info.name || '--';
    if (platformEl) platformEl.textContent = info.platform || '--';
    if (uaEl) uaEl.textContent = info.ua || '--';
    if (coresEl) coresEl.textContent = info.cores || '--';
    if (memoryEl) memoryEl.textContent = info.memory || '--';
    if (resEl) resEl.textContent = info.resolution || '--';
    if (typeEl) typeEl.textContent = info.type || '--';
}
