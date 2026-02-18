#!/usr/bin/env python3
"""Diagnostic script to verify real metrics are being collected."""

import sys
from pathlib import Path
import json

# Add backend src to path
backend_src = Path(__file__).parent / "BACKEND" / "src"
sys.path.insert(0, str(backend_src))

print("="*60)
print("CLOUD GAMING OPTIMIZER - REAL METRICS VERIFICATION")
print("="*60)

# Test 1: Check if psutil is available
print("\n[1] Checking dependencies...")
try:
    import psutil
    print(f"✅ psutil {psutil.__version__} installed")
    HAS_PSUTIL = True
except ImportError:
    print("❌ psutil NOT installed - will use mock data")
    HAS_PSUTIL = False

try:
    import GPUtil
    print(f"✅ GPUtil installed")
    HAS_GPUTIL = True
except ImportError:
    print("⚠️  GPUtil NOT installed - GPU metrics will use fallback")
    HAS_GPUTIL = False

# Test 2: Test SystemMetricsCollector
print("\n[2] Testing SystemMetricsCollector...")
try:
    from data_collection.system_metrics import SystemMetricsCollector
    collector = SystemMetricsCollector()
    metrics = collector.collect_all_metrics()
    
    cpu = metrics['cpu']['cpu_percent']
    ram = metrics['memory']['ram_percent']
    disk = metrics['disk']['disk_percent']
    
    print(f"✅ SystemMetricsCollector working:")
    print(f"   - CPU: {cpu:.1f}%")
    print(f"   - RAM: {ram:.1f}%")
    print(f"   - Disk: {disk:.1f}%")
    print(f"   - GPU Available: {metrics['gpu']['gpu_available']}")
    
    # Check if using real values (not mock)
    if HAS_PSUTIL:
        print(f"   ✅ Using REAL system metrics (psutil enabled)")
    else:
        print(f"   ⚠️  Using MOCK fallback metrics (psutil not available)")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Test NetworkMetricsCollector
print("\n[3] Testing NetworkMetricsCollector...")
try:
    from data_collection.network_metrics import NetworkMetricsCollector
    collector = NetworkMetricsCollector()
    metrics = collector.collect_all_metrics()
    
    latency = metrics['ping']['ping_ms']
    jitter = metrics['ping']['jitter_ms']
    packet_loss = metrics['ping']['packet_loss_percent']
    
    print(f"✅ NetworkMetricsCollector working:")
    print(f"   - Latency: {latency:.1f} ms")
    print(f"   - Jitter: {jitter:.2f} ms")
    print(f"   - Packet Loss: {packet_loss:.2f}%")
    
    if latency != 25.0 or packet_loss != 0.1:
        print(f"   ✅ Using REAL network measurements")
    else:
        print(f"   ⚠️  Using default/mock network values (ping may not be available)")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Test Flask API endpoint
print("\n[4] Testing Flask API...")
try:
    sys.path.insert(0, str(Path(__file__).parent / "FRONTEND"))
    from web_app import app
    
    with app.test_client() as client:
        response = client.get('/api/metrics')
        data = response.get_json()
        
        if data['success']:
            cpu = data['system']['cpu_percent']
            ram = data['system']['ram_percent']
            latency = data['network']['ping_ms']
            
            print(f"✅ Flask API working:")
            print(f"   - Endpoint: GET /api/metrics")
            print(f"   - CPU: {cpu:.1f}%")
            print(f"   - RAM: {ram:.1f}%")
            print(f"   - Latency: {latency:.1f} ms")
            
            if cpu > 0.1 or ram > 0.1:
                print(f"   ✅ API returning REAL metrics")
            else:
                print(f"   ⚠️  API may be returning mock/zero values")
        else:
            print(f"❌ API error: {data}")
            
except Exception as e:
    print(f"❌ Error testing Flask: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)
print("\nIf you see ✅ REAL metrics above, then:")
print("  1. Your system metrics ARE being collected")
print("  2. The Flask API IS returning real values")
print("  3. If the dashboard still shows mock values:")
print("     - Check browser console (F12) for any errors")
print("     - Try Ctrl+Shift+R to hard refresh (clear cache)")
print("     - Redeploy your cloud app with latest code")
print("\nIf you see ⚠️ warnings:")
print("  - The app is using mock fallback values")
print("  - This is normal in containerized environments")
print("  - Real metrics will work fine on user systems")
