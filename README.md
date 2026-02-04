# Recommendation System Monitoring Stack

A complete Docker-based monitoring and alerting solution for a FastAPI recommendation engine using Prometheus and Grafana.

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- 3 available ports: 8000 (API), 9090 (Prometheus), 3000 (Grafana)

### Deploy

```bash
docker compose up -d
```

### Access Services

- **FastAPI API:** http://localhost:8000
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000

---

## 📋 What's Included

### 1. **FastAPI Recommendation Engine** (`app/main.py`)

A REST API that generates recommendations with built-in Prometheus metrics.

**Endpoints:**

- `GET /recommend` - Get recommended posts
- `GET /metrics` - Prometheus metrics

**Metrics Tracked:**

- `recommendation_requests_total` - Total API requests
- `recommendation_latency_seconds` - Request latency histogram
- `recommendation_errors_total` - Failed requests

**Features:**

- Random latency simulation (0.1-1.0s)
- 20% simulated error rate
- Prometheus-formatted metrics output

### 2. **Prometheus** (`prometheus/prometheus.yml`)

Time-series database that collects metrics from the API.

**Configuration:**

- Scrape interval: 5 seconds
- Auto-discovers metrics from `http://app:8000/metrics`
- Stores all historical data

### 3. **Grafana** (`grafana/provisioning/`)

Visualization and alerting platform.

**Pre-configured:**

- Prometheus datasource automatically connected
- "High Latency" alert rule (P95 > 0.3s)
- Email notifications via Gmail SMTP

---

## 🏗️ Project Structure

```
monitoring-stack/
├── docker-compose.yml              # Service orchestration
├── README.md                        # This file
├── app/
│   └── main.py                     # FastAPI application
├── prometheus/
│   └── prometheus.yml              # Prometheus configuration
└── grafana/
    └── provisioning/
        ├── alerting/
        │   └── alerts.yaml         # Alert rules
        └── datasources/
            └── grafana-datasource.yaml  # Prometheus datasource
```

---

## 🔧 Key Commands

### Start Stack

```bash
docker compose up -d
```

### Stop Stack

```bash
docker compose down
```

### View Logs

```bash
docker compose logs -f [service]
# Examples:
docker compose logs -f recsys_app
docker compose logs -f prometheus
docker compose logs -f grafana
```

### Check Status

```bash
docker compose ps
```

### Restart Services

```bash
docker compose restart
```

### View Metrics

```bash
# From host
curl http://localhost:8000/metrics

# From inside API container
docker compose exec recsys_app curl http://localhost:8000/metrics
```

---

## 📊 Monitoring & Alerts

### Predefined Alert: High Recommendation Latency

- **Trigger:** 95th percentile latency > 0.3 seconds for 2+ minutes
- **Query:** `histogram_quantile(0.95, rate(recommendation_latency_seconds_bucket[1m])) > 0.3`
- **Action:** Email notification to `miraclinvinnarasi@gmail.com`

### Test the Alert

```bash
# Generate load to trigger alert
for i in {1..100}; do
  curl http://localhost:8000/recommend &
done
wait
```

---

## 📈 Useful PromQL Queries

Paste these in Prometheus (http://localhost:9090) or Grafana:

```promql
# Request rate per minute
rate(recommendation_requests_total[1m])

# 95th percentile latency
histogram_quantile(0.95, rate(recommendation_latency_seconds_bucket[1m]))

# Error rate (percentage)
(rate(recommendation_errors_total[1m]) / rate(recommendation_requests_total[1m])) * 100

# Total errors
recommendation_errors_total

# Service availability (opposite of error rate)
1 - (rate(recommendation_errors_total[1m]) / rate(recommendation_requests_total[1m]))
```

---

## 🔐 Security Notes

⚠️ **IMPORTANT for Production:**

- Gmail credentials are exposed in `docker-compose.yml` - use environment variables instead
- Configure authentication in Grafana
- Use persistent volumes for Prometheus data
- Set resource limits for containers
- Consider adding reverse proxy/authentication layer

---

## 🐛 Troubleshooting

### Containers won't start

```bash
# Check logs
docker compose logs

# Ensure ports are free
netstat -ano | findstr :8000
netstat -ano | findstr :9090
netstat -ano | findstr :3000
```

### Can't access API

```bash
# Check if container is running
docker ps | grep recsys_app

# Check container logs
docker logs recsys_app
```

### Prometheus not scraping metrics

```bash
# Check Prometheus targets
# Visit: http://localhost:9090/targets

# Or check logs
docker logs prometheus
```

### Grafana alerts not working

```bash
# Verify datasource is connected
# In Grafana: Configuration > Data Sources > Prometheus

# Check alert logs
docker logs grafana
```

---

## 📝 Configuration Files

### `docker-compose.yml`

- Defines 3 services: app, prometheus, grafana
- Maps ports and volumes
- Sets environment variables for SMTP

### `app/main.py`

- FastAPI application
- Defines metrics and endpoints
- Can be modified to track custom metrics

### `prometheus/prometheus.yml`

- Scrape configuration
- Change `scrape_interval` to adjust collection frequency
- Add new scrape jobs for additional services

### `grafana/provisioning/alerting/alerts.yaml`

- Alert rule definitions
- Modify thresholds and conditions
- Add new alert rules as needed

### `grafana/provisioning/datasources/grafana-datasource.yaml`

- Datasource configuration
- Auto-provisions Prometheus on startup

---

## 🚦 What's Happening?

1. **API Server starts** → Generates metrics in Prometheus format
2. **Prometheus scrapes** → Every 5 seconds, pulls metrics from API
3. **Data is stored** → Time-series data saved in Prometheus DB
4. **Grafana visualizes** → Reads data from Prometheus for dashboards/alerts
5. **Alerts trigger** → When conditions are met, notifications are sent

---

## 📚 Next Steps

1. **Create Dashboards** in Grafana to visualize metrics
2. **Test Alerts** by generating load on the API
3. **Monitor Logs** to understand system behavior
4. **Customize Metrics** in `app/main.py` for your use case
5. **Add More Alerts** in `alerts.yaml` as needed
6. **Deploy to Production** with proper security measures

---

## 📖 Documentation

See `SETUP_DOCUMENTATION.md` for detailed technical documentation.

---

## 🤝 Support

For issues or questions:

- Check logs: `docker compose logs`
- Verify services: `docker compose ps`
- Review configuration files for syntax errors
- Visit Prometheus targets page: http://localhost:9090/targets

---

**Stack Status:** ✅ Running
**Last Updated:** February 4, 2026
