"""Web Application - Flask-based Dashboard for Cloud Gaming Optimizer."""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, jsonify, Response

# Add backend src to path - handles both local and deployed environments
# We need to add the BACKEND/src directory to sys.path
import os
current_file = Path(__file__).resolve()  # /path/to/FRONTEND/web_app.py
current_dir = current_file.parent  # /path/to/FRONTEND
parent_dir = current_dir.parent  # /path/to/
backend_src = parent_dir / "BACKEND" / "src"

if backend_src.exists():
    sys.path.insert(0, str(backend_src))
else:
    # Try alternative: Maybe we're deployed and working from root
    cwd_parent = Path.cwd().parent
    alt_backend_src = cwd_parent / "BACKEND" / "src"
    if alt_backend_src.exists():
        sys.path.insert(0, str(alt_backend_src))

# Lazy imports to avoid import-time failures
app = Flask(__name__, 
            template_folder=str(Path(__file__).parent / 'templates'),
            static_folder=str(Path(__file__).parent / 'static'),
            static_url_path='/static')
app.config['SECRET_KEY'] = 'cloud-gaming-optimizer-secret-key'

# Setup logging
log_path = Path("logs/web_app.log")
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@app.after_request
def add_client_hints(response: Response):
    """Add Accept-CH response header to request additional client hints.

    Note: Browsers will only send UA Client Hints when they respect this header
    and the site is served over HTTPS. This helps `navigator.userAgentData`
    provide higher-entropy values on supported browsers.
    """
    try:
        # Request platform, model, architecture and mobile hints
        response.headers['Accept-CH'] = 'Sec-CH-UA, Sec-CH-UA-Platform, Sec-CH-UA-Model, Sec-CH-UA-Arch, Sec-CH-UA-Mobile'
        response.headers['Accept-CH-Lifetime'] = '86400'
    except Exception:
        pass
    return response


@app.route('/api/client_hints')
def get_client_hints():
    """Return parsed UA Client Hints and related headers sent by the browser.

    Browsers will only send these headers if they received an `Accept-CH` header
    previously and over HTTPS. This endpoint helps the frontend augment device
    detection with server-observed hints.
    """
    from flask import request

    hints = {
        'sec_ch_ua': request.headers.get('Sec-CH-UA'),
        'sec_ch_ua_platform': request.headers.get('Sec-CH-UA-Platform'),
        'sec_ch_ua_model': request.headers.get('Sec-CH-UA-Model'),
        'sec_ch_ua_arch': request.headers.get('Sec-CH-UA-Arch'),
        'sec_ch_ua_mobile': request.headers.get('Sec-CH-UA-Mobile'),
        'user_agent': request.headers.get('User-Agent')
    }

    # Normalize simple values
    # Sec-CH-UA values often come quoted; strip surrounding quotes if present
    def _clean(v):
        if not v:
            return None
        return v.strip().strip('"')

    for k in list(hints.keys()):
        hints[k] = _clean(hints[k])

    return jsonify({'success': True, 'hints': hints, 'timestamp': datetime.now().isoformat()})

# Global components (initialized on first request)
_network_collector = None
_system_collector = None
_optimizer = None
_monitor = None
_alert_system = None
_rules = None


def get_components():
    """Get or initialize components lazily."""
    global _network_collector, _system_collector, _optimizer, _monitor, _alert_system, _rules
    
    if _network_collector is None:
        try:
            from data_collection.network_metrics import NetworkMetricsCollector
            from data_collection.system_metrics import SystemMetricsCollector
            from optimization_engine.optimizer import GamingOptimizer
            from optimization_engine.optimization_rules import OptimizationRules
            from monitoring.performance_monitor import PerformanceMonitor
            from monitoring.alert_system import AlertSystem
            
            _network_collector = NetworkMetricsCollector()
            _system_collector = SystemMetricsCollector()
            _rules = OptimizationRules()
            _optimizer = GamingOptimizer(optimization_rules=_rules)
            _monitor = PerformanceMonitor()
            _alert_system = AlertSystem()
            
            logger.info("Components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
    
    return {
        'network': _network_collector,
        'system': _system_collector,
        'optimizer': _optimizer,
        'monitor': _monitor,
        'alert_system': _alert_system
    }


@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('index.html')


@app.route('/api/metrics')
def get_metrics():
    """Get current network and system metrics."""
    try:
        components = get_components()
        
        # Collect metrics
        net_data = components['network'].collect_all_metrics()
        sys_data = components['system'].collect_all_metrics()
        
        # Extract ping metrics
        net_metrics = net_data.get('ping', {})
        
        # Extract system metrics
        cpu = sys_data.get('cpu', {})
        memory = sys_data.get('memory', {})
        gpu = sys_data.get('gpu', {})
        disk = sys_data.get('disk', {})
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'network': {
                'ping_ms': net_metrics.get('ping_ms', 0),
                'jitter_ms': net_metrics.get('jitter_ms', 0),
                'packet_loss_percent': net_metrics.get('packet_loss_percent', 0),
                'min_latency_ms': net_metrics.get('min_latency_ms', 0),
                'max_latency_ms': net_metrics.get('max_latency_ms', 0)
            },
            'system': {
                'cpu_percent': cpu.get('cpu_percent', 0),
                'cpu_count': cpu.get('cpu_count', 0),
                'cpu_freq_ghz': cpu.get('cpu_freq_ghz', 0),
                'ram_percent': memory.get('ram_percent', 0),
                'ram_used_gb': memory.get('ram_used_gb', 0),
                'ram_total_gb': memory.get('ram_total_gb', 0),
                'ram_available_gb': memory.get('ram_available_gb', 0),
                'gpu_available': gpu.get('gpu_available', False),
                'gpu_percent': gpu.get('gpu_percent', 0),
                'gpu_memory_percent': gpu.get('gpu_memory_percent', 0),
                'gpu_name': gpu.get('gpu_name', 'N/A'),
                'gpu_count': gpu.get('gpu_count', 0),
                'disk_percent': disk.get('disk_percent', 0),
                'disk_used_gb': disk.get('disk_used_gb', 0),
                'disk_total_gb': disk.get('disk_total_gb', 0)
            },
            'system_health': components['system'].get_system_health()
        })
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/optimize')
def get_optimization():
    """Get optimization recommendations."""
    try:
        components = get_components()
        
        # Collect metrics
        net_data = components['network'].collect_all_metrics()
        sys_data = components['system'].collect_all_metrics()
        
        # Extract ping metrics
        net_metrics = net_data.get('ping', {})
        
        # Get system metrics for optimizer
        sys_for_optimizer = {
            'cpu_percent': sys_data.get('cpu', {}).get('cpu_percent', 0),
            'ram_percent': sys_data.get('memory', {}).get('ram_percent', 0),
            'gpu_percent': sys_data.get('gpu', {}).get('gpu_percent', 0),
            'gpu_available': sys_data.get('gpu', {}).get('gpu_available', False)
        }
        
        # Get optimization result
        result = components['optimizer'].optimize(net_metrics, sys_for_optimizer)
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'recommendations': result.get('recommendations', {}),
            'current_quality': result.get('current_quality', 'unknown'),
            'optimization_reason': result.get('reason', '')
        })
    except Exception as e:
        logger.error(f"Error getting optimization: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/alerts')
def get_alerts():
    """Get current alerts."""
    try:
        components = get_components()
        
        # Collect metrics
        net_data = components['network'].collect_all_metrics()
        sys_data = components['system'].collect_all_metrics()
        
        # Extract metrics for alert check
        net_metrics = net_data.get('ping', {})
        sys_for_alerts = {
            'cpu_percent': sys_data.get('cpu', {}).get('cpu_percent', 0),
            'ram_percent': sys_data.get('memory', {}).get('ram_percent', 0),
            'gpu_percent': sys_data.get('gpu', {}).get('gpu_percent', 0)
        }
        
        # Check for new alerts
        new_alerts = components['alert_system'].check_metrics(net_metrics, sys_for_alerts)
        
        # Get recent alerts
        recent_alerts = components['alert_system'].get_recent_alerts(limit=10)
        
        alerts_list = []
        for alert in recent_alerts:
            alerts_list.append({
                'level': alert.level.name,
                'message': alert.message,
                'metric': alert.metric,
                'value': alert.value,
                'threshold': alert.threshold,
                'timestamp': alert.timestamp
            })
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'alert_count': len(alerts_list),
            'alerts': alerts_list
        })
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats')
def get_stats():
    """Get performance statistics."""
    try:
        components = get_components()
        
        # Get current stats
        stats = components['monitor'].get_current_stats()
        
        # Also collect some basic metrics for additional stats
        net_data = components['network'].collect_all_metrics()
        sys_data = components['system'].collect_all_metrics()
        
        net_metrics = net_data.get('ping', {})
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'stats': stats,
            'latency_ms': net_metrics.get('ping_ms', 0),
            'jitter_ms': net_metrics.get('jitter_ms', 0),
            'fps': stats.get('current_fps', 60)
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history')
def get_history():
    """Get metrics history for charts."""
    try:
        components = get_components()
        
        # Get metrics history from monitor
        history = components['monitor'].get_history(limit=60)
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'history': history
        })
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


def run_server(host=None, port=None, debug=None):
    """Run the Flask server.
    
    Supports environment variables for cloud deployment:
    - HOST: Server host (default: 0.0.0.0 for cloud, 127.0.0.1 for local)
    - PORT: Server port (default: 5000)
    - FLASK_ENV: Flask environment (production/development)
    """
    import os
    
    # Get from environment or use defaults
    host = host or os.environ.get('HOST', '0.0.0.0')
    port = port or int(os.environ.get('PORT', 5000))
    flask_env = os.environ.get('FLASK_ENV', 'development')
    debug = debug if debug is not None else (flask_env != 'production')
    
    logger.info(f"Starting Cloud Gaming Optimizer Web Dashboard on {host}:{port}")
    logger.info(f"Environment: {flask_env}")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server()
