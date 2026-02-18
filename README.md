# ☁️ Cloud Gaming Optimizer

A real-time performance monitoring and optimization tool for cloud gaming environments. Monitor network metrics (latency, jitter, packet loss) and system resources (CPU, RAM, GPU, Disk) with intelligent optimization recommendations.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask Web App](https://img.shields.io/badge/Framework-Flask-green)

---

## ✨ Features

- 🌐 **Real-time Network Metrics**
  - Latency monitoring (Ping times)
  - Jitter analysis
  - Packet loss detection
  - Network health visualization

- 🖥️ **System Performance Monitoring**
  - CPU usage and frequency
  - RAM utilization
  - GPU metrics (when available)
  - Disk I/O and space
  - Real-time health status

- 🎮 **Gaming Optimization**
  - Intelligent resolution recommendations
  - Target FPS optimization
  - Bitrate suggestions
  - Quality vs. Performance balancing

- 📊 **Advanced Analytics**
  - Performance history charts
  - System health alerts
  - Interactive dashboard
  - Real-time updates

- 🔔 **Alert System**
  - Performance warnings
  - Resource threshold alerts
  - Network anomaly detection
  - Color-coded severity levels

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Linux/Windows/Mac

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MRADUL142/CLOUD_GAMING_OPTIMIZER_.git
   cd CLOUD_GAMING_OPTIMIZER_
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web dashboard:**
   ```bash
   cd FRONTEND
   python web_app.py
   ```

4. **Open in browser:**
   ```
   http://localhost:5000
   ```

---

## 📁 Project Structure

```
CLOUD_GAMING_OPTIMIZER_/
├── FRONTEND/
│   ├── web_app.py              # Flask web application
│   ├── requirements.txt          # Python dependencies
│   ├── templates/
│   │   └── index.html           # Dashboard HTML template
│   └── static/
│       ├── css/
│       │   └── style.css        # Dashboard styling
│       └── js/
│           └── app.js           # Frontend logic
│
├── BACKEND/
│   ├── main.py                  # CLI main entry point
│   ├── service.py               # Background service
│   ├── config/
│   │   └── settings.yaml        # Configuration
│   ├── src/
│   │   ├── data_collection/     # Metrics collection
│   │   ├── optimization_engine/ # Optimization logic
│   │   └── monitoring/          # Alert system
│   └── tests/
│       └── test_basic.py        # Unit tests
│
├── DEPLOYMENT_GUIDE.md          # Cloud deployment guide
├── Procfile                      # Cloud platform configuration
└── README.md                     # This file
```

---

## 🌐 Live Demo & Deployment

### Try Online (Static Preview)
- **Dashboard Preview:** https://mradul142.github.io/CLOUD_GAMING_OPTIMIZER_/dashboard.html
- Shows demo data with full styling and charts

### Deploy Your Own (Free Options)
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete instructions.

**Quick Deploy to Railway.app (Recommended):**
1. Fork this repository
2. Go to https://railway.app
3. Connect your GitHub account
4. Select this repository
5. Railway auto-deploys!
6. Your app is live at: `https://[project-name].up.railway.app`

**Other Options:**
- Render.com (Free tier, sleeps after 15 min)
- PythonAnywhere (Python-optimized hosting)
- Fly.io (Global edge locations)
- DigitalOcean (Affordable VPS)

---

## 📖 Usage

### Web Dashboard
Access the interactive dashboard at `http://localhost:5000`

**Sections:**
- **Network Metrics:** Real-time latency, jitter, packet loss
- **System Metrics:** CPU, RAM, GPU, Disk usage
- **Optimization Panel:** Smart recommendations for gaming
- **Alerts:** System warnings and anomalies
- **Performance Charts:** Historical trends

### CLI Usage (Backend)
```bash
cd BACKEND

# Run dashboard mode
python main.py --dashboard

# Run optimization once
python main.py --optimize

# Run alerts check
python main.py --alerts

# Collect raw metrics
python main.py --collect
```

---

## ⚙️ Configuration

Edit `BACKEND/config/settings.yaml` to customize:

```yaml
network:
  ping_host: "8.8.8.8"
  timeout: 4
  count: 4

system:
  cpu_threshold: 80
  ram_threshold: 85
  gpu_threshold: 90

monitoring:
  alert_level: "warning"
  history_size: 1000
```

---

## 📊 API Endpoints

If running with Flask:

```
GET  /                 # Main dashboard
GET  /api/metrics      # Current system & network metrics
GET  /api/optimize     # Optimization recommendations
GET  /api/alerts       # Recent alerts
GET  /api/stats        # Performance statistics
GET  /api/history      # Metrics history
GET  /health           # Health check
```

---

## 🛠️ Development

### Run Tests
```bash
cd BACKEND
python -m pytest tests/
```

### Code Structure
- `/src/data_collection/` - Metric collectors
- `/src/optimization_engine/` - Optimization logic
- `/src/monitoring/` - Alert system
- `FRONTEND/web_app.py` - Flask application

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 🎯 Performance Insights

The optimizer provides recommendations based on:
- **Network Latency** (0-300ms range)
- **Jitter Values** (stability analysis)
- **Packet Loss** (connection quality)
- **CPU Usage** (processing power)
- **RAM Availability** (memory headroom)
- **GPU Capacity** (rendering power)

Each metric affects the recommended gaming quality settings.

---

## 🔍 System Requirements

- **Minimum:** 2GB RAM, 100MB disk space
- **Recommended:** 4GB RAM, 500MB disk space
- **Network:** Active internet connection (for metrics)

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Areas for contribution:
- Additional metrics (CPU frequency scaling, process monitoring)
- More optimization rules for different games
- Database support for long-term analytics
- Mobile app version
- Docker containerization

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review DEPLOYMENT_GUIDE.md for deployment help

---

## 🔮 Roadmap

- [ ] Machine learning-based optimization
- [ ] Historical data persistence
- [ ] Multi-user support
- [ ] REST API documentation
- [ ] Docker container
- [ ] Mobile app
- [ ] Game-specific profiles
- [ ] VPN integration

---

## 👨‍💻 Author

**MRADUL142**
- GitHub: [@MRADUL142](https://github.com/MRADUL142)
- Project: [CLOUD_GAMING_OPTIMIZER_](https://github.com/MRADUL142/CLOUD_GAMING_OPTIMIZER_)

---

## 🌟 Show Your Support

Give a ⭐️ if this project helps you with cloud gaming optimization!

```
Made with ❤️ for cloud gaming enthusiasts
```
