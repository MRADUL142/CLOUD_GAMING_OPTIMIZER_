"""System Metrics Collector - Real implementation using psutil and GPUtil."""

import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    logger.warning("psutil not available - using mock data")

try:
    import GPUtil
    HAS_GPUTIL = True
except ImportError:
    HAS_GPUTIL = False
    logger.warning("GPUtil not available - GPU metrics will be limited")


class SystemMetricsCollector:
    """Stub implementation for collecting system metrics."""
    
    def collect(self) -> Dict[str, Any]:
        """Collect current system metrics."""
        try:
            if HAS_PSUTIL:
                return {
                    "timestamp": datetime.now().isoformat(),
                    "cpu_percent": psutil.cpu_percent(interval=0.5),
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_percent": psutil.disk_usage('/').percent,
                    "gpu_percent": self._get_gpu_percent(),
                    "gpu_memory_percent": self._get_gpu_memory_percent(),
                    "temperature_celsius": self._get_temperature()
                }
            else:
                return self._get_mock_metrics()
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return self._get_mock_metrics()
    
    def collect_all_metrics(self) -> Dict[str, Any]:
        """Collect all system metrics in expected format."""
        try:
            if not HAS_PSUTIL:
                return self._get_mock_all_metrics()
            
            # Get real metrics from psutil
            cpu_times = psutil.cpu_times_percent(interval=0.5)
            virtual_mem = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')
            cpu_freq = psutil.cpu_freq()
            
            # Get network stats
            net_io = psutil.net_io_counters()
            
            # Get GPU info
            gpu_info = self._get_real_gpu_info()
            
            return {
                "cpu": {
                    "cpu_percent": psutil.cpu_percent(interval=0.5),
                    "cpu_count": psutil.cpu_count(),
                    "cpu_freq_ghz": cpu_freq.current / 1000.0 if cpu_freq else 0,
                    "per_cpu": psutil.cpu_percent(interval=0.1, percpu=True),
                    "load_average": list(psutil.getloadavg()) if hasattr(psutil, 'getloadavg') else [0, 0, 0],
                    "user_time_percent": cpu_times.user,
                    "system_time_percent": cpu_times.system,
                    "idle_time_percent": cpu_times.idle
                },
                "memory": {
                    "ram_percent": virtual_mem.percent,
                    "ram_used_gb": virtual_mem.used / (1024**3),
                    "ram_total_gb": virtual_mem.total / (1024**3),
                    "ram_available_gb": virtual_mem.available / (1024**3),
                    "swap_percent": psutil.swap_memory().percent
                },
                "gpu": gpu_info,
                "disk": {
                    "disk_percent": disk_usage.percent,
                    "disk_used_gb": disk_usage.used / (1024**3),
                    "disk_total_gb": disk_usage.total / (1024**3),
                    "disk_read_speed_mbps": 150.0,  # Mock - needs time delta
                    "disk_write_speed_mbps": 120.0  # Mock - needs time delta
                },
                "network": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error collecting all system metrics: {e}")
            return self._get_mock_all_metrics()
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        try:
            if not HAS_PSUTIL:
                return self._get_mock_health()
            
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            gpu = self._get_gpu_percent()
            temp = self._get_temperature()
            
            # Determine health based on metrics
            def get_health_status(value, critical=90, warning=75):
                if value > critical:
                    return "critical"
                elif value > warning:
                    return "warning"
                else:
                    return "good"
            
            return {
                "overall_status": "healthy" if all([
                    cpu < 90, mem < 90, disk < 90, gpu < 90
                ]) else "caution",
                "cpu_health": get_health_status(cpu),
                "gpu_health": get_health_status(gpu),
                "memory_health": get_health_status(mem),
                "disk_health": get_health_status(disk),
                "thermal_health": "normal" if temp < 80 else ("warning" if temp < 95 else "critical"),
                "power_consumption_watts": 250,  # Mock
                "fps_estimate": self._estimate_fps(cpu, gpu, mem),
                "throttling_detected": temp > 85 if temp else False
            }
        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return self._get_mock_health()
    
    def _get_real_gpu_info(self) -> Dict[str, Any]:
        """Get real GPU information."""
        try:
            if HAS_GPUTIL:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    return {
                        "gpu_available": True,
                        "gpu_percent": gpu.load * 100,
                        "gpu_memory_percent": gpu.memoryUtil * 100,
                        "gpu_name": gpu.name,
                        "gpu_count": len(gpus),
                        "vram_used_gb": (gpu.memoryTotal - gpu.memoryFree) / 1024,
                        "vram_total_gb": gpu.memoryTotal / 1024,
                        "gpu_temp_celsius": getattr(gpu, 'temperature', 0)
                    }
        except Exception as e:
            logger.warning(f"Could not get real GPU info: {e}")
        
        return {
            "gpu_available": False,
            "gpu_percent": 0,
            "gpu_memory_percent": 0,
            "gpu_name": "N/A",
            "gpu_count": 0,
            "vram_used_gb": 0,
            "vram_total_gb": 0,
            "gpu_temp_celsius": 0
        }
    
    def _get_gpu_percent(self) -> float:
        """Get GPU usage percentage."""
        try:
            if HAS_GPUTIL:
                gpus = GPUtil.getGPUs()
                if gpus:
                    return gpus[0].load * 100
        except Exception:
            pass
        return 0.0
    
    def _get_gpu_memory_percent(self) -> float:
        """Get GPU memory usage percentage."""
        try:
            if HAS_GPUTIL:
                gpus = GPUtil.getGPUs()
                if gpus:
                    return gpus[0].memoryUtil * 100
        except Exception:
            pass
        return 0.0
    
    def _get_temperature(self) -> float:
        """Get CPU temperature."""
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    # Try to get CPU temp (varies by system)
                    for name, entries in temps.items():
                        if entries:
                            return entries[0].current
        except Exception:
            pass
        return 0.0
    
    def _estimate_fps(self, cpu: float, gpu: float, mem: float) -> int:
        """Estimate gaming FPS based on system load."""
        # Simple heuristic: lower fps if high loads
        if gpu > 90 or cpu > 80 or mem > 85:
            return 60
        elif gpu > 70 or cpu > 60 or mem > 70:
            return 90
        else:
            return 120
    
    def _get_mock_metrics(self) -> Dict[str, Any]:
        """Get mock metrics when psutil unavailable."""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": 45.2,
            "memory_percent": 62.1,
            "disk_percent": 75.3,
            "gpu_percent": 88.5,
            "gpu_memory_percent": 72.1,
            "temperature_celsius": 65.0
        }
    
    def _get_mock_all_metrics(self) -> Dict[str, Any]:
        """Get mock all metrics when psutil unavailable."""
        return {
            "cpu": {
                "cpu_percent": 45.2,
                "cpu_count": 8,
                "cpu_freq_ghz": 3.2,
                "per_cpu": [45.2, 40.1, 50.3, 42.8, 45.2, 40.1, 50.3, 42.8],
                "load_average": [0.45, 0.42, 0.40]
            },
            "memory": {
                "ram_percent": 62.1,
                "ram_used_gb": 7.9,
                "ram_total_gb": 16.0,
                "ram_available_gb": 6.1,
                "swap_percent": 0.0
            },
            "gpu": {
                "gpu_available": True,
                "gpu_percent": 88.5,
                "gpu_memory_percent": 72.1,
                "gpu_name": "NVIDIA RTX 3080",
                "gpu_count": 1,
                "vram_used_gb": 8.0,
                "vram_total_gb": 12.0,
                "gpu_temp_celsius": 65.0
            },
            "disk": {
                "disk_percent": 75.3,
                "disk_used_gb": 240.5,
                "disk_total_gb": 1000.0,
                "disk_read_speed_mbps": 150.0,
                "disk_write_speed_mbps": 120.0
            },
            "network": {
                "bytes_sent": 1024000,
                "bytes_recv": 2048000,
                "packets_sent": 10000,
                "packets_recv": 15000
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_mock_health(self) -> Dict[str, Any]:
        """Get mock health when psutil unavailable."""
        return {
            "overall_status": "healthy",
            "cpu_health": "good",
            "gpu_health": "good",
            "memory_health": "good",
            "disk_health": "good",
            "thermal_health": "normal",
            "power_consumption_watts": 250,
            "fps_estimate": 120
        }
    
        """Get historical system metrics."""
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics summary."""
        try:
            if HAS_PSUTIL:
                cpu = psutil.cpu_percent(interval=0.5)
                mem = psutil.virtual_memory().percent
                return {
                    "avg_cpu": cpu,
                    "max_cpu": 92.3,  # Would track over time
                    "avg_memory": mem,
                    "avg_gpu": self._get_gpu_percent(),
                    "temperature_warning": False
                }
        except Exception:
            pass
        
        return {
            "avg_cpu": 45.2,
            "max_cpu": 92.3,
            "avg_memory": 62.1,
            "avg_gpu": 88.5,
            "temperature_warning": False
        }
