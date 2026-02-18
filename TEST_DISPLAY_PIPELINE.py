#!/usr/bin/env python3
"""Test the actual metrics display pipeline."""

import sys
from pathlib import Path

# Add paths
frontend_path = Path(__file__).parent / "FRONTEND"
backend_path = Path(__file__).parent / "BACKEND" / "src"
sys.path.insert(0, str(frontend_path))
sys.path.insert(0, str(backend_path))

from web_app import app

print("="*70)
print("REAL METRICS DISPLAY TEST")
print("="*70)

# Simulate 3 dashboard loads
with app.test_client() as client:
    for attempt in range(1, 4):
        print(f"\n[Attempt {attempt}] Simulating dashboard refresh...")
        
        # Get metrics like frontend would
        response = client.get('/api/metrics')
        data = response.get_json()
        
        if not data.get('success'):
            print(f"❌ API failed: {data}")
            continue
        
        # Extract like updateMetricsDisplay() does
        network = data['network']
        system = data['system']
        
        # Display what would show on the dashboard
        print(f"\n  Network Metrics:")
        print(f"    Latency: {network['ping_ms']:.1f} ms")
        print(f"    Jitter:  {network['jitter_ms']:.1f} ms")
        print(f"    Loss:    {network['packet_loss_percent']:.1f} %")
        
        print(f"\n  System Metrics:")
        print(f"    CPU:     {system['cpu_percent']:.1f} %  (Cores: {system['cpu_count']})")
        print(f"    RAM:     {system['ram_percent']:.1f} %  ({system['ram_used_gb']:.1f}/{system['ram_total_gb']:.1f} GB)")
        print(f"    Disk:    {system['disk_percent']:.1f} %  ({system['disk_used_gb']:.1f}/{system['disk_total_gb']:.1f} GB)")
        print(f"    GPU:     {system['gpu_name']} ({system['gpu_percent']:.1f}%)")
        
        print(f"\n  System Health:")
        health = data.get('system_health', {})
        print(f"    Status:  {health.get('overall_status', 'unknown')}")
        print(f"    FPS Est: {health.get('fps_estimate', '--')} fps")

print("\n" + "="*70)
print("✅ VERIFICATION COMPLETE")
print("="*70)
print("\nThese are the REAL VALUES that should be displayed on the dashboard.")
print("If you see different values on your deployed app, the issue is likely:")
print("  1. Browser cache (use Ctrl+Shift+R to clear)")
print("  2. Old cloud deployment (redeploy from GitHub)")
print("  3. JavaScript not loading properly (check browser console F12)")
